Install AgentOS into the CURRENT Git repository using the AgentOS v3 OKF installer specification.

Trusted installer source (Git URL or locally unpacked path):
<TRUSTED_INSTALLER_REPOSITORY_URL_OR_LOCAL_PATH>

Pinned source revision (Git commit/tag, or an explicitly trusted local snapshot):
<PINNED_COMMIT_OR_RELEASE>

Find and read `INSTALL.md` at that source, then follow its linked OKF v0.2 bundle entrypoint, constitutional requirements, progressive graph-navigation rules, and adaptive interview process. Treat installer documents as read-only reference material; do not execute scripts fetched from the installer automatically. If you cannot access or verify the source, report the blocker rather than inventing its contents.

Begin with READ-ONLY discovery of the current target repository and its agent runtime. Conduct a brief conversational initial interview. Based on repository evidence and user answers, load only relevant OKF components, ask their local follow-up questions, and recursively resolve hard dependencies. Present the tailored implementation plan and affected paths before making target repository changes; obtain authorization for mutations and external effects. Implement only selected, necessary capabilities; use native runtime configurations where appropriate, preserve existing content, minimize top-level clutter, validate actual behavior, and hand off to the permanent root Director. OKF metadata is not itself executable permission or technical enforcement.
