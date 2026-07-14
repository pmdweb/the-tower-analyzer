# 0001 — Save container

## Scope

This document records only observations validated against a locally extracted `playerInfo.dat` sample. Raw samples are intentionally excluded from Git.

## Confirmed structure

```text
playerInfo.dat
└── GZip stream
    └── binary payload
        └── probable .NET NRBF/BinaryFormatter record stream
```

The observed root type name is expected to be `SaveLoad+PlayerData` from the game's Unity `Assembly-CSharp` domain. This must be revalidated by the future NRBF reader rather than hard-coded as trusted input.

## Security constraints

- Never invoke `BinaryFormatter` or native .NET deserialization on an uploaded save.
- Parse records as untrusted bytes.
- Enforce compressed and decompressed size limits.
- Reject malformed lengths, invalid references, and unsupported record types.
- Never modify, restore, or write to a player's save file.
- Do not commit raw saves or IL2CPP metadata extracted from a device.

## Current implementation

The `inspect` command currently:

1. validates the GZip magic bytes;
2. calculates a SHA-256 digest of the original file;
3. decompresses with an output-size ceiling;
4. reports basic metadata;
5. performs no object deserialization.

## Next investigation

Implement an NRBF record scanner that can enumerate record types, libraries, class metadata, object IDs, and references without constructing executable runtime objects.
