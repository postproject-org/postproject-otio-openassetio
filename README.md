# PostProject OTIO-through-OpenAssetIO validation

This focused integration stores a PostProject entity reference in an ordinary OTIO
`ExternalReference` and resolves it through the upstream `otio-openassetio`
linker plus the PostProject Manager validation. There is intentionally no
PostProject-specific OTIO plugin.

The SDK uses `RepresentationRef(id)` to create the host binding.
The persisted entity-reference text and OTIO payload remain compatible.

This checkout requires the PostProject 0.9 development wheel and matching
native library. Install the pinned media linker used by CI before running
the test; it is a separate upstream package.
