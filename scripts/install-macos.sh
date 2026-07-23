#!/usr/bin/env bash
# install-macos.sh — bootstrap a roots_seed Forest workspace on macOS, natively.
#
# Installs the terminal toolchain, Claude Code (and optionally the Desktop app that hosts
# Cowork), and lays out a workspace with its `.roots/` memory ready to use.
#
#   /bin/bash -c "$(curl -fsSL <raw-url>/scripts/install-macos.sh)"        # one-liner
#   ./install-macos.sh --workspace ~/forest                                # from a checkout
#   ./install-macos.sh --check                                             # diagnose only
#
# Options:
#   --workspace <path>  where the Forest lives            (default: ~/forest)
#   --profile <name>    minimal | standard | full         (default: standard)
#   --no-claude         skip installing Claude Code
#   --desktop           also install the Claude Desktop app (Cowork lives there)
#   --check             report what is installed/missing and exit (changes nothing)
#   -n, --dry-run       print what would run
#   -y, --yes           no prompts
#
# Profiles:
#   minimal   git jq ripgrep coreutils gnu-sed bash
#   standard  + fd gawk python3 gh tree wget          <- what the seed's own scripts use
#   full      + node pandoc ffmpeg imagemagick        <- reporting, media, JS tooling
#
# Safe to re-run: every step checks before acting. Nothing is installed with sudo except
# Apple's Command Line Tools and Homebrew's own installer, which ask for their own consent.
set -euo pipefail

WORKSPACE="${HOME}/forest"; PROFILE="standard"; DO_CLAUDE=1; DO_DESKTOP=0
CHECK_ONLY=0; DRY=0; ASSUME_YES=0
SEED_REPO="${ROOTS_SEED_REPO:-https://github.com/ctmil/roots_seed.git}"

# ---------- ui ----------
if [ -t 1 ]; then B=$'\033[1m'; G=$'\033[32m'; Y=$'\033[33m'; R=$'\033[31m'; D=$'\033[2m'; Z=$'\033[0m'
else B=""; G=""; Y=""; R=""; D=""; Z=""; fi
say()  { printf '%s\n' "$*"; }
step() { printf '\n%s==>%s %s%s%s\n' "$G" "$Z" "$B" "$*" "$Z"; }
ok()   { printf '  %s✓%s %s\n' "$G" "$Z" "$*"; }
warn() { printf '  %s!%s %s\n' "$Y" "$Z" "$*"; }
err()  { printf '  %s✗%s %s\n' "$R" "$Z" "$*"; }
info() { printf '  %s%s%s\n' "$D" "$*" "$Z"; }
die()  { printf '\n%serror:%s %s\n' "$R" "$Z" "$*" >&2; exit 1; }
run()  { if [ "$DRY" -eq 1 ]; then printf '  %s[dry-run]%s %s\n' "$D" "$Z" "$*"; else eval "$@"; fi; }
have() { command -v "$1" >/dev/null 2>&1; }

ask() {  # ask "question" -> 0=yes
  [ "$ASSUME_YES" -eq 1 ] && return 0
  [ -t 0 ] || return 1
  printf '  %s? %s [y/N] %s' "$Y" "$1" "$Z"; read -r a || return 1
  case "$a" in y|Y|yes|Yes) return 0 ;; *) return 1 ;; esac
}

while [ $# -gt 0 ]; do
  case "$1" in
    --workspace) WORKSPACE="${2:?}"; shift ;;
    --profile)   PROFILE="${2:?}"; shift ;;
    --no-claude) DO_CLAUDE=0 ;;
    --desktop)   DO_DESKTOP=1 ;;
    --check)     CHECK_ONLY=1 ;;
    -n|--dry-run) DRY=1 ;;
    -y|--yes)    ASSUME_YES=1 ;;
    -h|--help)   sed -n '2,30p' "$0"; exit 0 ;;
    *) die "unknown option: $1 (see --help)" ;;
  esac
  shift
done

case "$PROFILE" in minimal|standard|full) ;; *) die "unknown profile: $PROFILE" ;; esac

PKGS_MINIMAL="git jq ripgrep coreutils gnu-sed bash"
PKGS_STANDARD="fd gawk python@3.12 gh tree wget"
PKGS_FULL="node pandoc ffmpeg imagemagick"
case "$PROFILE" in
  minimal)  PKGS="$PKGS_MINIMAL" ;;
  standard) PKGS="$PKGS_MINIMAL $PKGS_STANDARD" ;;
  full)     PKGS="$PKGS_MINIMAL $PKGS_STANDARD $PKGS_FULL" ;;
esac

# ---------- 0. platform ----------
step "Checking the platform"
[ "$(uname -s)" = "Darwin" ] || die "this script is for macOS. On Linux/WSL use scripts/setup-module.sh directly."
OSV="$(sw_vers -productVersion 2>/dev/null || echo '?')"
OSMAJOR="${OSV%%.*}"
ARCH="$(uname -m)"
ok "macOS $OSV ($ARCH)"
if [ "$OSMAJOR" != "?" ] && [ "$OSMAJOR" -lt 13 ] 2>/dev/null; then
  warn "Claude Code requires macOS 13.0+. The toolchain will still install."
fi
[ "$ARCH" = "arm64" ] && BREW_PREFIX="/opt/homebrew" || BREW_PREFIX="/usr/local"

# ---------- check mode ----------
if [ "$CHECK_ONLY" -eq 1 ]; then
  step "Environment report"
  for t in brew git claude jq rg fd gawk python3 gh pandoc ffmpeg node tree wget; do
    if have "$t"; then ok "$(printf '%-9s %s' "$t" "$(command -v "$t")")"; else err "$(printf '%-9s missing' "$t")"; fi
  done
  say ""
  info "bash: $BASH_VERSION  (macOS ships 3.2 as /bin/bash — brew installs 5.x)"
  have gsed && ok "gsed present (GNU sed — scripts written for GNU need it)" || warn "gsed missing: BSD sed differs from GNU (\`sed -i\` needs an argument)"
  [ -d "$WORKSPACE" ] && ok "workspace exists: $WORKSPACE" || warn "workspace not created yet: $WORKSPACE"
  [ -d "$WORKSPACE/.roots" ] && ok ".roots/ present" || warn ".roots/ not initialized"
  exit 0
fi

# ---------- 1. Command Line Tools ----------
step "Apple Command Line Tools"
if xcode-select -p >/dev/null 2>&1; then
  ok "already installed ($(xcode-select -p))"
else
  warn "not installed — macOS will open its own dialog"
  run "xcode-select --install || true"
  say ""
  info "Finish the install in that dialog, then re-run this script."
  [ "$DRY" -eq 1 ] || exit 0
fi

# ---------- 2. Homebrew ----------
step "Homebrew"
if have brew; then
  ok "$(brew --version | head -1)"
else
  warn "not installed"
  if ask "Install Homebrew now? (it will ask for your password)"; then
    run '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  else
    die "Homebrew is required for the native toolchain. Re-run when ready."
  fi
fi
# make brew usable in THIS shell and in future ones (Apple Silicon puts it outside the default PATH)
if [ -x "$BREW_PREFIX/bin/brew" ]; then
  eval "$("$BREW_PREFIX/bin/brew" shellenv)"
  for rc in "$HOME/.zprofile" "$HOME/.bash_profile"; do
    [ -e "$rc" ] || continue
    if ! grep -q 'brew shellenv' "$rc" 2>/dev/null; then
      run "printf '\neval \"\$(%s/bin/brew shellenv)\"\n' '$BREW_PREFIX' >> '$rc'"
      ok "added brew to $(basename "$rc")"
    fi
  done
  # zsh is the macOS default shell but .zprofile may not exist yet
  if [ ! -e "$HOME/.zprofile" ]; then
    run "printf 'eval \"\$(%s/bin/brew shellenv)\"\n' '$BREW_PREFIX' > '$HOME/.zprofile'"
    ok "created ~/.zprofile with brew in PATH"
  fi
fi

# ---------- 3. toolchain ----------
step "Terminal toolchain (profile: $PROFILE)"
TO_INSTALL=""
for p in $PKGS; do
  if brew list --formula --versions "$p" >/dev/null 2>&1; then ok "$p"; else TO_INSTALL="$TO_INSTALL $p"; fi
done
if [ -n "$TO_INSTALL" ]; then
  info "installing:$TO_INSTALL"
  run "brew install $TO_INSTALL"
else
  ok "everything already present"
fi

step "macOS-vs-GNU notes (this is where portable scripts usually break)"
info "• /bin/bash is 3.2 (2007). Scripts using \${var,,}, associative arrays or 'readarray'"
info "  need the brew bash: put #!/usr/bin/env bash and make sure $BREW_PREFIX/bin is first in PATH."
info "• BSD sed/date/awk differ from GNU: 'sed -i' REQUIRES an argument on macOS ('sed -i \"\" …')."
info "  Portable fix: write the script for GNU and use gsed/gdate/gawk, or opt into the gnubin PATH:"
info "    export PATH=\"$BREW_PREFIX/opt/coreutils/libexec/gnubin:$BREW_PREFIX/opt/gnu-sed/libexec/gnubin:\$PATH\""
if ask "Add that gnubin PATH line to ~/.zprofile? (makes GNU tools the default in your shell)"; then
  run "printf '\nexport PATH=\"%s/opt/coreutils/libexec/gnubin:%s/opt/gnu-sed/libexec/gnubin:\$PATH\"\n' '$BREW_PREFIX' '$BREW_PREFIX' >> '$HOME/.zprofile'"
  ok "added — it applies to new terminals"
else
  info "skipped: keep using gsed/gdate/gawk explicitly in scripts"
fi

# ---------- 4. Claude Code ----------
if [ "$DO_CLAUDE" -eq 1 ]; then
  step "Claude Code (CLI)"
  if have claude; then
    ok "already installed: $(claude --version 2>/dev/null || echo 'version unknown')"
  else
    info "the native installer keeps itself updated in the background; the brew cask does not"
    run 'curl -fsSL https://claude.ai/install.sh | bash'
    # the native installer puts the launcher in ~/.local/bin
    case ":$PATH:" in
      *":$HOME/.local/bin:"*) ;;
      *) run "printf '\nexport PATH=\"\$HOME/.local/bin:\$PATH\"\n' >> '$HOME/.zprofile'"
         ok "added ~/.local/bin to PATH in ~/.zprofile"
         export PATH="$HOME/.local/bin:$PATH" ;;
    esac
    have claude && ok "installed: $(claude --version 2>/dev/null)" || warn "open a new terminal, then check with: claude --version"
  fi
  info "first run: 'claude' opens the browser to log in (needs a paid plan)"
  info "diagnostics without starting a session: claude doctor"
fi

if [ "$DO_DESKTOP" -eq 1 ]; then
  step "Claude Desktop app (this is where Cowork runs)"
  if [ -d "/Applications/Claude.app" ]; then
    ok "already installed"
  elif brew info --cask claude >/dev/null 2>&1; then
    run "brew install --cask claude"
  else
    warn "no cask available — download it from https://claude.com/download"
    run "open 'https://claude.com/download' || true"
  fi
fi

# ---------- 5. workspace ----------
step "Forest workspace: $WORKSPACE"
run "mkdir -p '$WORKSPACE'"
cd "$WORKSPACE" 2>/dev/null || { [ "$DRY" -eq 1 ] || die "cannot enter $WORKSPACE"; }

if [ -d "$WORKSPACE/roots_seed/.git" ] || [ -d "$WORKSPACE/roots_seed/main/.git" ] || [ -f "$WORKSPACE/roots_seed/main/.git" ]; then
  ok "roots_seed already present"
  SEED_DIR="$WORKSPACE/roots_seed/main"; [ -d "$SEED_DIR" ] || SEED_DIR="$WORKSPACE/roots_seed"
else
  info "cloning the seed from $SEED_REPO"
  run "git clone --depth 1 '$SEED_REPO' '$WORKSPACE/roots_seed'"
  SEED_DIR="$WORKSPACE/roots_seed"
fi

if [ ! -d "$WORKSPACE/.git" ]; then
  run "git -C '$WORKSPACE' init -q"
  ok "workspace initialized as a git repo (the coordination layer is versioned too)"
fi

step "Fleet scripts at the workspace root"
for s in setup-module.sh setupbranch.sh dashboard.sh pull-all.sh sync-agents-skills.sh; do
  if [ -e "$WORKSPACE/$s" ]; then ok "$s (kept — not overwritten)"
  elif [ -e "$SEED_DIR/scripts/$s" ]; then run "cp '$SEED_DIR/scripts/$s' '$WORKSPACE/$s'"; run "chmod +x '$WORKSPACE/$s'"; ok "$s"
  fi
done

# ---------- 6. .roots skeleton (lazy: only what every deployment needs) ----------
step ".roots/ memory"
if [ -d "$WORKSPACE/.roots" ]; then
  ok "already initialized (untouched)"
else
  run "mkdir -p '$WORKSPACE/.roots/state'"
  [ -e "$SEED_DIR/roots_seed.md" ] && run "cp '$SEED_DIR/roots_seed.md' '$WORKSPACE/.roots/roots_seed.md'"
  TODAY="$(date +%Y-%m-%d)"
  if [ "$DRY" -eq 0 ]; then
    cat > "$WORKSPACE/.roots/_meta.json" <<EOF
{
  "layout": "flat",
  "working_mode": "workspace",
  "lang": "en",
  "seed_version": "1.15",
  "created": "$TODAY",
  "platform": "macos"
}
EOF
    cat > "$WORKSPACE/.roots/context.md" <<'EOF'
# Workspace - Context

> 30-second briefing. Keep it short: this is read at the start of every session.

## What this is
<one paragraph: what this Forest coordinates>

## Stack
<languages, runtimes, platforms>

## Current state
<what is being worked on right now — details go in state/>

## Key conventions
- Memory lives in `.roots/`, tracked. Secrets (`*.secret`, `*.local.env`) are gitignored.
- A server is always *a commit*: branch per task -> commit -> deploy = fetch + checkout.
  See `roots_seed.md` § Deploy discipline.
- Where the work stands right now: `state/`. What happened: `journal/`.

## Folders are created lazily
Only `_meta.json`, `context.md`, `roots_seed.md` and `state/` exist at bootstrap. Create
`docs/`, `design/`, `journal/`, `tasks/`, `debug/`, `skills/`, `agents/` on their first real use.
EOF
    cat > "$WORKSPACE/.roots/state/comms.md" <<'EOF'
# comms — inter-session message bus

> Append-only, newest on top. One block per message. Read this at session start and before any
> push/sync. See `roots_seed.md` § Inter-session comms.

## <ISO-8601> · from: install · to: @all · re: workspace bootstrap · status: open
Workspace created by `install-macos.sh`. Fill in `.roots/context.md` before real work starts.
EOF
  fi
  ok "created: _meta.json, context.md, state/comms.md, roots_seed.md"
fi

# ---------- 7. gitignore ----------
step ".gitignore"
GI="$WORKSPACE/.gitignore"
if [ -e "$GI" ] && grep -q 'roots/\*\*/\*.secret' "$GI" 2>/dev/null; then
  ok "already carries the .roots rules"
elif [ "$DRY" -eq 0 ]; then
  cat >> "$GI" <<'EOF'

# --- .roots memory: tracked WHOLESALE, then secrets re-excluded ---
# order matters: the re-exclusions must come AFTER the un-ignore, or they do not apply.
!.roots/
!.roots/**
.roots/**/*.secret
.roots/**/*.local.env
.roots/**/secrets.local.env
.roots/**/__pycache__/
.roots/**/*.pyc

# activation layer is local, not shared
.claude/settings.local.json
.claude/**/*.secret
.claude/**/*.local.env

# macOS
.DS_Store
EOF
  ok "written"
else
  info "[dry-run] would append the .roots/.claude/macOS rules"
fi

# ---------- 8. activation layer ----------
step "Activation layer (.claude/)"
run "mkdir -p '$WORKSPACE/.claude/agents' '$WORKSPACE/.claude/skills'"
if [ -d "$SEED_DIR/agents" ]; then
  info "base library available at $SEED_DIR/agents — import on demand, do not preload:"
  info "  ./sync-agents-skills.sh import bug-hunter grove-keeper --seed '$SEED_DIR'"
  info "  ./sync-agents-skills.sh activate"
fi

# ---------- 9. CLAUDE.md + Cowork entry point ----------
step "Entry points for the assistant"
if [ -e "$WORKSPACE/CLAUDE.md" ]; then
  ok "CLAUDE.md exists (untouched)"
elif [ "$DRY" -eq 0 ]; then
  cat > "$WORKSPACE/CLAUDE.md" <<'EOF'
# CLAUDE.md — Forest workspace

Persistent memory lives in **`.roots/`** (tool-agnostic markdown). `.roots/` is the source of
truth; this file is only a bridge for Claude Code.

## Start here
- `.roots/context.md` — what this workspace is (30 s)
- `.roots/state/` — where the work stands **now**; `state/comms.md` = messages between sessions
- `.roots/roots_seed.md` — the memory spec itself

## Hard rules
- **Deploy is git-first**: branch per task → commit → the server does `fetch` + `checkout <commit>`.
  Never write files into a versioned checkout. The work branch pushes automatically; **merging to
  the deploy branch and deploying are confirmed with the human.**
- Secrets never get committed (`*.secret`, `*.local.env` are gitignored).
- Read-only sources stay read-only.

## Sessions
At session close, update `.roots/` (`state/`, and `journal/` if something happened worth keeping).
EOF
  ok "CLAUDE.md"
fi

if [ ! -e "$WORKSPACE/README.md" ] && [ "$DRY" -eq 0 ]; then
  cat > "$WORKSPACE/README.md" <<EOF
# Forest workspace

Persistent agent memory in \`.roots/\` (see \`.roots/roots_seed.md\`).

## Two ways to work on this folder

**Claude Code (terminal)** — full local power: runs the fleet scripts, git, builds and deploys.
\`\`\`bash
cd "$WORKSPACE" && claude
\`\`\`

**Claude Cowork (Desktop app)** — no terminal needed. Open the Claude Desktop app and **connect
this folder** so Claude can read and write it; the app must stay open for local file access.
Cowork reads and writes the \`.roots/\` markdown like any other file, which is the point of keeping
the memory tool-agnostic. Two caveats worth knowing before you rely on it:

- Cowork runs code in an **isolated environment on Anthropic's servers**, not in your shell — so it
  is not the tool for running the fleet scripts against your local repos or for deploying. Use
  Claude Code for anything that has to touch this machine or a server.
- Cowork's support for \`CLAUDE.md\` and for skills is **not documented** as of this writing; do not
  assume it auto-loads them. \`.roots/context.md\` is plain markdown — point Cowork at it explicitly
  at the start of a session, or paste it in.

Rule of thumb: **Cowork for document-shaped work over the memory** (research, drafts, organizing,
summaries) and **Claude Code for anything that runs**.
EOF
  ok "README.md (includes the Cowork ↔ Claude Code split)"
fi

# ---------- done ----------
step "Done"
say ""
say "  Workspace : ${B}$WORKSPACE${Z}"
say "  Seed      : $SEED_DIR"
say "  Profile   : $PROFILE"
say ""
say "  Next:"
say "    1. ${B}open a new terminal${Z} (so the PATH changes apply)"
say "    2. cd '$WORKSPACE' && claude          ${D}# log in on first run${Z}"
say "    3. edit .roots/context.md             ${D}# tell it what this Forest is${Z}"
say "    4. ./setup-module.sh <name> <git-url> <branch...>   ${D}# mount your first Tree${Z}"
say ""
say "  ${D}Re-run with --check any time to diagnose the environment.${Z}"
