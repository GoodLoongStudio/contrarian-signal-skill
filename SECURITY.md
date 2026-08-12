# Security Policy

## Scope

Contrarian Signal operates on public information and local deterministic calculations. It does not require brokerage credentials, wallet keys, trading permissions, or private financial account access.

## Sensitive data

Do not commit:

- API keys or access tokens;
- brokerage credentials;
- private portfolio exports containing unnecessary personal information;
- non-public market information;
- scraped session cookies or login secrets.

If private data is voluntarily supplied for a local analysis, minimize retention and do not include it in public examples, fixtures, issues, or commits.

## Trading boundary

The Skill must not execute trades or silently connect to brokerage/order APIs. Any future integration that can place, modify, or cancel orders must be treated as a separate capability with explicit user authorization and separate review.

## Reporting issues

For security or privacy concerns, open a private security advisory on the GitHub repository when available rather than posting secrets in a public issue.
