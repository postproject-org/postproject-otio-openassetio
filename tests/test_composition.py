"""Probe unmodified OTIO/OpenAssetIO composition with PostProject."""

import os

import opentimelineio as otio
from postproject import Production


def test_external_reference_resolves_without_postproject_linker(tmp_path):
    library = os.environ["POSTPROJECT_LIBRARY"]
    media = tmp_path / "plate.exr"
    media.write_bytes(b"frame")
    project = tmp_path / "show.pproj"
    with Production.create(project, library_path=library) as production:
        with production.transaction() as transaction:
            asset = transaction.import_media(media, "plate")
        representation = production.representations[asset][0]
        entity_reference = production.host_bindings[representation.id]

    clip = otio.schema.Clip(
        name="plate",
        media_reference=otio.schema.ExternalReference(target_url=entity_reference),
        source_range=otio.opentime.TimeRange(
            otio.opentime.RationalTime(1001, 24),
            otio.opentime.RationalTime(1, 24),
        ),
    )
    timeline = otio.schema.Timeline(name="validation")
    timeline.tracks.append(otio.schema.Track(children=[clip]))
    encoded = otio.adapters.write_to_string(timeline, adapter_name="otio_json")
    linked = otio.adapters.read_from_string(
        encoded,
        adapter_name="otio_json",
        media_linker_name="openassetio_media_linker",
        media_linker_argument_map={
            "identifier": "org.postproject.manager-validation",
            "settings": {
                "production_path": str(project),
                "library_path": library,
            },
        },
    )

    linked_clip = linked.find_clips()[0]
    assert linked_clip.media_reference.target_url == media.resolve().as_uri()
    assert linked_clip.source_range.start_time == otio.opentime.RationalTime(1001, 24)
