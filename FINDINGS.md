# Findings

- The three existing extension points compose unchanged: OTIO carries the URL,
  its upstream media linker requests `LocatableContent`, and the Manager asks
  PostProject to resolve the representation.
- The linker mutates only `target_url`; the clip's rational time remains OTIO's
  responsibility and round-trips intact.
- The upstream linker currently handles `ExternalReference` only. Sequence
  structure therefore belongs in OpenAssetIO traits until the linker gains an
  `ImageSequenceReference` mapping.
- With OpenAssetIO-MediaCreation 1.0.0a13, the pinned upstream linker emits a
  deprecation warning because it imports the unversioned location trait.
- The linker's cached Manager context is keyed by argument maps, so production
  path and library settings must be explicit and stable.
