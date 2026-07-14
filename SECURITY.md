# Security policy

## Supported versions

The project is in early development. Security fixes apply to the latest commit on `main`.

## Untrusted input

All save files and metadata files are untrusted binary input. Contributors must not:

- execute or natively deserialize save payloads;
- use .NET `BinaryFormatter` to load uploaded data;
- disable decompression or allocation limits;
- commit real player saves, credentials, identifiers, or device metadata;
- implement save editing or restoration features.

## Reporting

Report suspected vulnerabilities privately to the repository owner. Do not attach real save files to public issues.
