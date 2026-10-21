# Authentication

Category: core-software-engineering · Topic ID: authentication

## Sources

- [could not fetch] https://roadmap.sh/guides/basic-authentication — only navigation/header image, actual article body did not render.
- [fetched] https://roadmap.sh/guides/session-based-authentication — real content, fully rendered (unlike its three sibling guide pages).
- [could not fetch] https://roadmap.sh/guides/token-authentication — only navigation/header image, actual article body did not render.
- [could not fetch] https://roadmap.sh/guides/jwt-authentication — only navigation/header image, actual article body did not render.

## Findings

**What session-based authentication is, the one resource that actually rendered** (roadmap.sh):
a stateful method where the server tracks authenticated users via sessions, working around
HTTP's inherent statelessness. Flow: (1) user submits credentials; (2) server validates, creates
a session, stores client info (memory/filesystem/database), generates a unique session ID;
(3) server sends the ID to the client, stored as a cookie, sent on every subsequent request;
(4) server looks up the session ID on each request to retrieve the client's info. Key benefit:
"the server has a way to associate some information with the client" without requiring
re-authentication on every request.

**Honest gap**: the roadmap doc's own topic description frames authentication broadly —
passwords, API keys, OAuth 2.0, JWTs — and distinguishes authentication (identity) from
authorization (permissions). Three of this topic's four specific guide pages (basic auth,
token-based auth, JWT auth) failed to render their actual explanatory content despite being
the same roadmap.sh guide format that rendered successfully for session-based auth — an
inconsistent, not fully explained, rendering failure across sibling pages on the same site.
Only session-based auth is genuinely documented here; basic/token/JWT auth are known only by
name, not by mechanism, from this research pass.

**Direct relevance to this system**: this project's own authentication is simpler than any of
these four mechanisms — it relies on the `gh` CLI's existing authenticated session (the
user's own GitHub login), not a custom auth layer the system itself implements. This topic is
background for a future engagement that requires building authentication from scratch, not
something this system currently needs to solve itself.

## Practitioner notes (you)

(left empty — the user adds their own experience here, not the agent)
