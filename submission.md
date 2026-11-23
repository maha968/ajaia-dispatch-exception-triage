# Ajaia Technical Project Manager Assessment

**Video:** [(https://youtu.be/q68dCpXF7H4)]

**Engagement:** Corrigan Peak Logistics — Dispatch Exception Triage  
**Reference:** https://ajaia.ai

## Task 1 — Triage

1. **B — Retry/concurrency duplicate routing: WORK THIS WEEK.** Hold Priya's PR from merging until she implements and tests idempotent routing, including a durable deduplication key, recovery after a successful queue push but failed database update, and overlapping poll cycles. Duplicate assignments can create conflicting dispatcher actions; test failures before release.
2. **C — Terminal 3 EDI schema mismatch (DET-121): WORK THIS WEEK.** Escalate the unanswered 8/6 request to Corrigan Peak IT and Dana for a named owner and field definitions today. Null urgency scores compromise triage; budget the stated two additional days after confirmation and test Terminal 3 end-to-end, including missing-field handling.
3. **D — Terminal lead routing-rules review (DET-118): WORK THIS WEEK.** Marcus or the account team should contact all three terminal leads immediately, offer concrete review slots, and track approval of routing rules before launch. It is not a technical blocker today, but an unowned acceptance dependency can become one.
4. **A — Auto-reassignment after missed pickup: DEFER from September 8 scope.** This is a new write/action workflow, not an extension of exception flagging; it requires authority rules, backup-carrier eligibility, auditability, failure handling, and client acceptance tests. Offer a scoped discovery and post-launch change proposal rather than committing the board date without impact analysis.
5. **E — Dispatcher UI shade of blue: DEFER.** This is **noise** relative to data integrity, dispatch correctness, and launch acceptance; revisit after launch unless terminal users demonstrate an accessibility or usability issue.

**Schedule protection:** Keep September 8 as the target, not an unconditional promise. Prioritize B and C; run DET-118 scheduling in parallel; exclude A and E from the release. Reassess the critical path once Corrigan Peak IT confirms the mapping and Priya estimates the routing fix. If validated testing and terminal signoff cannot fit, escalate an explicit scope/date decision to Dana rather than silently compressing QA.

## Task 2 — Working build

**Files:** `normalize_exceptions.py` (executable Python 3 script), `exceptions.csv` (provided sample), `cleaned_exceptions.csv` (generated output), `exception_summary.txt` (generated report).

**Run:** `python normalize_exceptions.py exceptions.csv --output cleaned_exceptions.csv --summary exception_summary.txt`

The script reads the provided CSV, normalizes `T3` and `Terminal 3` to `Terminal 3`, uppercases carrier codes, and converts three recognized timestamp formats to ISO-8601-like formatting while preserving whether a source timestamp explicitly specifies UTC (`Z`). It writes cleaned records and a count by event type. I checked the actual output against all five source rows: five rows remain; `missed_pickup=2`, `doc_mismatch=2`, and `carrier_substitution=1`; `swft`, `SWFT`, and `Swft` become `SWFT`. **CPX-88216 cannot be fully cleaned** because its carrier code is blank, so it is flagged rather than guessed. Four timestamps lack timezone information; they are consistently formatted but deliberately not labeled UTC. This cleanup does not establish the correct FreightWorks EDI field mapping or itself resolve DET-121.

## Task 3 — Client status update

**To:** Dana Okafor, VP Operations, Corrigan Peak Logistics  
**Subject:** Dispatch Exception Triage — September 8 readiness and actions this week

Hi Dana,

I want to correct the picture in last Friday's Green status update. We described the Terminal 3 feed issue as minor and reported no blockers. That was too confident: Terminal 3 is returning null urgency scores for some exceptions, and the field mapping has been awaiting confirmation since August 6. We also identified a routing retry/concurrency risk in code review that could send the same exception to a dispatcher queue more than once. **Current status: Amber / At Risk.**

Our September 8 go-live remains the target, but we are not calling it assured until these issues are resolved and tested. This week Priya will address and test duplicate-routing prevention before merging her change. We need a named Corrigan Peak IT contact to confirm Terminal 3's actual EDI fields as soon as possible; once we have that answer, the current estimate is two additional days to correct the mismatch, followed by validation. We are also contacting all three terminal leads now to schedule routing-rules reviews and obtain their feedback before launch.

On the COO's missed-pickup auto-reassignment request: I understand the value, but automatically moving freight to a backup carrier introduces new authorization, operational, and failure-handling requirements. I recommend keeping dispatcher-directed triage in the September 8 release and scoping auto-reassignment as a separately approved follow-on change. We will also defer the requested queue color adjustment unless it proves to be a usability/accessibility issue.

I will send you a revised readiness assessment and any schedule or scope tradeoff once we have the IT mapping confirmation and Priya's tested fix estimate. If the remaining work threatens September 8, we will bring you options and a recommendation promptly rather than reduce testing without your knowledge.

Could you help identify the Corrigan Peak IT owner for Terminal 3 today?

Thank you,  
Technical Project Manager  
Ajaia

## Task 4 — AI workflow note

I used ChatGPT to challenge my triage order, scaffold the CSV normalization script, and refine the client status language. I retained responsibility for the release-scope decisions, risk escalation, acceptance criteria, and what I would tell Dana. I specifically rejected treating all parsed timestamps as UTC: only one source record has an explicit `Z`, and inventing timezone certainty would create misleading data. I also verified the generated counts and reviewed the unresolved blank carrier field instead of accepting successful script execution as proof of correct data.
