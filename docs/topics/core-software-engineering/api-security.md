# API Security

Category: core-software-engineering · Topic ID: api-security

## Sources

- [fetched, via redirect] https://owasp.org/API-Security/editions/2023/en/0x00-toc/ → redirected (308) to https://api-security.owasp.org/editions/2023/en/0x00-toc — real content, the authoritative source for this topic.

## Findings

**The OWASP API Security Top 10 (2023 edition), the complete named list**:
1. **Broken Object Level Authorization** — authorization failures at the object level (a user
   can access/modify an object they shouldn't).
2. **Broken Authentication** — weaknesses in the authentication mechanism itself — connects
   directly to `authentication.md`'s four mechanisms (basic/session/token/JWT) in this same
   category.
3. **Broken Object Property Level Authorization** — gaps at the individual-property level
   (correct object access but wrong field-level permissions).
4. **Unrestricted Resource Consumption** — uncontrolled resource usage (no rate limiting/
   quotas) enabling abuse or denial-of-service-style exhaustion.
5. **Broken Function Level Authorization** — flaws in which functions/endpoints a given role
   can call.
6. **Unrestricted Access to Sensitive Business Flows** — inadequate protection of critical
   operations (checkout, password reset) beyond simple authZ checks.
7. **Server Side Request Forgery (SSRF)** — an API induced to make unintended requests to
   internal/external systems on an attacker's behalf.
8. **Security Misconfiguration** — improper security setup/configuration (same category of
   risk already found generally in `security.md`'s OWASP LLM Top 10 from platform-infra-devops).
9. **Improper Inventory Management** — inadequate tracking of what API assets/versions
   actually exist and are exposed.
10. **Unsafe Consumption of APIs** — risk introduced when an API consumes *other* external
    APIs without properly validating their responses.

This is the 2023 revision of the original 2019 list, with some risks renamed/repositioned
based on updated threat data — explicitly a living, periodically-revised standard, not a
fixed document.

**Direct relevance to this system**: this project's own `cimcime.cli` is itself an internal
API surface (per `apis-design.md`'s finding). Several of these risks map directly: #2 (Broken
Authentication) is delegated entirely to `gh`'s own auth, not reimplemented — correctly
avoiding risk #2 by not building custom auth at all; #4 (Unrestricted Resource Consumption) is
relevant to any future rate-limiting concern against GitHub's own API quotas; #9 (Improper
Inventory Management) is mitigated by this project's own `roadmap.py` acting as the single
source of truth for "what topics/categories actually exist" rather than trusting ad-hoc
tracking.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
