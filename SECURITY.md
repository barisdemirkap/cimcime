# Security

Please report vulnerabilities privately through GitHub's "Report a vulnerability" (Security tab)
rather than a public issue. Never include tokens or personal data in reports.

Cimcime runs Claude Code agents that can execute commands. Run it with least privilege, review the
permissions you grant, and keep secrets out of the repository (`secrets/` and `cimcime.toml` are gitignored).
