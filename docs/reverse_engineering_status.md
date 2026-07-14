# Reverse Engineering Status

## playerInfo.dat Format

```
playerInfo.dat
  └─ GZip compressed
       └─ .NET BinaryFormatter (MS-NRBF)
            └─ Unity IL2CPP objects
                 └─ SaveLoad.PlayerData
```

## Stage 1 – GZip Decompression ✅

**Status: Complete.**

The outer GZip wrapper is successfully decompressed by `GzipParser`.

## Stage 2 – BinaryFormatter Header ✅

**Status: Partially complete.**

The MS-NRBF `SerializationHeaderRecord` (record type 0) is read and
validated. The `root_id` and version fields are extracted.

**Remaining work:**
- Parse `BinaryLibrary` records (record type 12)
- Parse `ClassWithMembersAndTypes` records (record type 5) for `SaveLoad.PlayerData`
- Recursively decode nested class records
- Decode all MS-NRBF primitive types (Int32, Int64, Single, Double, Boolean, String, …)
- Decode array records (`ArraySinglePrimitive`, `BinaryArray`)
- Resolve `MemberReference` cross-references

## Stage 3 – Unity IL2CPP Object Graph ⏳

**Status: Stubbed.**

`ObjectGraph` scaffolding exists. Reference resolution requires Stage 2
to emit all raw objects from the stream.

**Remaining work:**
- Receive complete list of `RawObject` records from Stage 2
- Build `object_id → RawObject` registry
- Resolve `MemberReference` records to their targets
- Handle circular references (none expected in this save format, but guard anyway)

## Stage 4 – SaveLoad.PlayerData Mapping ⏳

**Status: Stubbed.**

`SaveDataSerializer` exists but cannot populate fields until Stage 3
produces a complete object graph.

**Known PlayerData fields (from community research):**

> ⚠️ Field names below are **unconfirmed** – to be verified against the actual
> BinaryFormatter stream.

| C# Field | Expected Type | Mapped To |
|----------|---------------|-----------|
| `playerName` | `string` | `PlayerAccount.player_name` |
| `level` | `int` | `PlayerAccount.level` |
| `prestige` | `int` | `PlayerAccount.prestige` |
| `coins` | `double` | `PlayerAccount.coins` / `Economy.coins` |
| `gems` | `int` | `Economy.gems` |
| `highestWave` | `int` | `PlayerAccount.highest_wave` |
| `workshopUpgrades` | `int[]` | `Workshop.upgrades` |
| `labUpgrades` | `int[]` | `Labs.upgrades` |

## Tools Used

- Python `gzip` stdlib – GZip decompression
- Custom MS-NRBF parser – BinaryFormatter stream decoding
- Pydantic v2 – typed data models

## References

- [MS-NRBF Specification](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nrbf)
- [The Tower community Discord](https://discord.gg/the-tower) – field name research
