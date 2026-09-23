#!/usr/bin/env python3
"""Headway — Onboarding + Paywall (CR rebuild).

Skeleton: personalization loop (goal -> quiz -> short loader -> echoed plan) with a
commitment beat at the seam. Grounded in the ScreensDesign replay of Headway's live flow,
with the contradiction rules applied: no sign-up wall, no permission prompts before the
paywall, every captured answer consumed, and the paywall headline naming the user's goal.
"""
import json
import sys
import pathlib

REF = pathlib.Path(
    "/Users/paimon/.claude/plugins/cache/adapty/adapty-skills/a9df778bface/"
    "skills/flow-generator/references")
sys.path.insert(0, str(REF))
import flowkit as fk  # noqa: E402

HERE = pathlib.Path(__file__).parent
YEAR = "da22cffe-64c4-487e-ade1-e229d76b5aa7"   # "1 year"  (period: annual)
MONTH = "f4088450-45a8-4737-8db0-367e642d7dcb"  # "1 month" (period: monthly)

ids = fk.Ids()
E = ids  # every element id comes from ONE generator (one script per flow)


# --------------------------------------------------------------------------- theme
COLORS = [
    ("bg",       "Page",              "#F3F7FF"),
    ("card",     "Card",              "#FFFFFF"),
    ("cardLine", "Card hairline",     "#DDE7F7"),
    ("ink",      "Ink",               "#0E2246"),
    ("inkMid",   "Ink mid",           "#4E627F"),
    ("inkSoft",  "Ink soft",          "#8494AC"),
    ("blue",     "Headway blue",      "#2563EB"),
    ("blueSoft", "Blue tint",         "#E3ECFF"),
    ("blueLine", "Blue line",         "#9FBEFB"),
    ("onBlue",   "On blue",           "#FFFFFF"),
    ("green",    "Green",             "#16A34A"),
    ("greenSoft","Green tint",        "#E3F6EA"),
    ("gold",     "Star gold",         "#F5A623"),
    ("amber",    "Badge amber",       "#FF7A2F"),
    ("onAmber",  "On amber",          "#FFFFFF"),
    ("quote",    "Quote card",        "#FFF8EC"),
]

TYPO = [
    # id, name, size, weight, lineHeight, letterSpacing
    ("eyebrow", "Eyebrow",       12, "bold",     15, 1.2),
    ("h1",      "Screen title",  28, "bold",     34, None),
    ("h2",      "Section title", 22, "bold",     27, None),
    ("h3",      "Card title",    18, "bold",     23, None),
    ("rowT",    "Row title",     16, "semibold", 21, None),
    ("body",    "Body",          15, "regular",  21, None),
    ("small",   "Small",         13, "regular",  18, None),
    ("legal",   "Legal",         11, "regular",  15, None),
    ("btn",     "Button",        17, "bold",     21, None),
    ("plan",    "Plan name",     17, "bold",     22, None),
    ("planSub", "Plan sub",      13, "regular",  17, None),
    ("price",   "Price",         20, "bold",     24, None),
    ("badge",   "Badge",         10, "bold",     13, 0.7),
    ("pwTitle", "Paywall title", 26, "bold",     31, None),
    ("stat",    "Stat",          24, "bold",     29, None),
]

# Real Phosphor SVG lifted from CampRoute Pro in the same app — never fabricated markup.
ICONS = json.loads((HERE / "icons.json").read_text())
# (name, weight) must match an entry in _meta.icons exactly, or the publish gate refuses it.
IW = {i["name"]: i["weight"] for i in ICONS}


# ------------------------------------------------------------------ progress bar
# Four quiz screens carry one dot each. This is the real progress-bar component wired
# through props.progressBar, not a row of decorative stacks.
PB_ID = "pb_dots"
PROGRESS = {PB_ID: {
    "map": {
        "el_pbBar": {"id": "el_pbBar", "type": "progress-bar", "states": [], "props": {
            "type": "multiple-segments", "template": "dots", "oneSegmentPerScreen": True,
            "width": fk.size("hug"), "height": fk.size("fixed", 8),
            "layout": fk.layout("horizontal", 7, "center", "center"),
            "position": fk.relative()}},
        "el_pbSeg": {"id": "el_pbSeg", "type": "progress-bar-segment", "states": [], "props": {
            "customId": "progress",
            "fill": fk.fill("cardLine"),
            "width": fk.size("fixed", 8), "height": fk.size("fixed", 8),
            "borderRadius": fk.radius(9999)}},
        "el_pbLoad": {"id": "el_pbLoad", "type": "progress-bar-loader", "states": [], "props": {
            "fill": fk.fill("blue"), "color": fk.color("blue"),
            "easing": "ease-in-out", "duration": 320,
            "position": fk.relative(), "borderRadius": fk.radius(9999)}},
    },
    "hierarchy": {"id": "root", "children": [
        {"id": "el_pbBar", "children": [
            {"id": "el_pbSeg", "children": [{"id": "el_pbLoad"}]}]}]}}}

# A component is referenced from a screen hierarchy as a node with NO entry in that screen's
# map — flowkit's flatten() has no notion of that, so the slot is built as a marker stack and
# swapped for the `global` node after the screen is assembled.
_MARKERS = set()


def pb_slot():
    mid = E("S")
    _MARKERS.add(mid)
    return fk.stack([fk.stack([], node_id=mid)],
                    width="fill", align_h="start", padding=fk.pad(2, 0, 0, 2),
                    node_id=E("S"))


def loader_el(duration_ms):
    """The real determinate `loader` element. A static filled stack looks identical in a
    screenshot and never advances — the fake-progress-bar shape patterns.md forbids."""
    return {"id": E("S"), "type": "loader", "states": [], "caption": "Progress",
            "props": {"fill": fk.fill("cardLine"), "color": fk.color("blue"),
                      "width": fk.size("fill"), "height": fk.size("fixed", 6),
                      "easing": "linear", "duration": duration_ms,
                      "position": fk.relative(), "borderRadius": fk.radius(3)}}


def mount_globals(scr):
    m = scr["elements"]["map"]

    def walk(node):
        kids = node.get("children") or []
        for i, k in enumerate(kids):
            if k["id"] in _MARKERS:
                m.pop(k["id"], None)
                kids[i] = {"id": PB_ID, "type": "global"}
            else:
                walk(k)

    walk(scr["elements"]["hierarchy"])
    return scr


# ------------------------------------------------------------------ small helpers
def cta(label, target=None, *, actions=None, sub=None, fill_id="bg"):
    """The pinned bottom bar: one full-width primary button, optional line under it."""
    button = fk.stack(
        [fk.stack([
            fk.text(fk.rich(label), preset="btn", color_id="onBlue", align="center",
                    width="hug", node_id=E("T")),
            fk.icon("ArrowRight", size_pt=17, color_id="onBlue", weight=IW["ArrowRight"],
                    node_id=E("I")),
        ], direction="horizontal", gap=8, align_h="center", align_v="center",
            width="hug", node_id=E("S"))],
        width="fill", fixed_h=56, corner=fk.radius(28), fill_=fk.fill("blue"),
        align_h="center", align_v="center",
        actions=actions if actions is not None else [fk.navigate(target)],
        node_id=E("S"))
    kids = [button]
    if sub:
        kids.append(fk.text(fk.rich(sub), preset="small", color_id="inkSoft",
                            align="center", node_id=E("T")))
    return fk.footer(kids, fill_=fk.fill(fill_id), padding=fk.pad(10, 20, 22, 20),
                     gap=10, node_id=E("S"))


def title_block(eyebrow, title, sub=None):
    out = []
    if eyebrow:
        out.append(fk.text(fk.rich(eyebrow), preset="eyebrow", color_id="blue",
                           node_id=E("T")))
    out.append(fk.text(fk.rich(*title) if isinstance(title, tuple) else fk.rich(title),
                       preset="h1", color_id="ink", node_id=E("T")))
    if sub:
        out.append(fk.text(fk.rich(sub), preset="body", color_id="inkMid", node_id=E("T")))
    return fk.stack(out, gap=8, node_id=E("S"))


def choice(group, custom_id, label, sub=None, default=False):
    """One quiz option. Base look is identical on every card; `selected` recolours it
    without changing any geometry (a border-width change reflows the whole column)."""
    kids = [fk.on_selected(
        fk.text(fk.rich(label), preset="rowT", color_id="ink", node_id=E("T")),
        color=fk.color("blue"))]
    if sub:
        kids.append(fk.on_selected(
            fk.text(fk.rich(sub), preset="small", color_id="inkSoft", node_id=E("T")),
            color=fk.color("inkMid")))
    return fk.on_selected(
        fk.selectable([fk.stack(kids, gap=2, node_id=E("S"))],
                      group_id=group, custom_id=custom_id, default=default,
                      width="fill", padding=fk.pad(15, 16, 16, 15),
                      corner=fk.radius(16), fill_=fk.fill("card"),
                      border="cardLine", align_v="center", node_id=E("S")),
        fill=fk.fill("blueSoft"),
        border={"color": fk.color("blue"), "style": "solid", "width": 1},
        padding=fk.pad(15, 16, 16, 15), borderRadius=fk.radius(16))


def bullet(icon_name, label, sub=None, tint="blueSoft", glyph="blue"):
    text_kids = [fk.text(fk.rich(label), preset="rowT", color_id="ink", node_id=E("T"))]
    if sub:
        text_kids.append(fk.text(fk.rich(sub), preset="small", color_id="inkMid",
                                 node_id=E("T")))
    return fk.stack([
        fk.stack([fk.icon(icon_name, size_pt=16, color_id=glyph, weight=IW[icon_name],
                          node_id=E("I"))],
                 fixed_w=32, fixed_h=32, corner=fk.radius(16), fill_=fk.fill(tint),
                 align_h="center", align_v="center", node_id=E("S")),
        fk.stack(text_kids, gap=1, node_id=E("S")),
    ], direction="horizontal", gap=12, align_v="center", node_id=E("S"))


def stars(n=5, size_pt=13):
    return fk.stack([fk.icon("Star", size_pt=size_pt, color_id="gold", weight=IW["Star"],
                             node_id=E("I")) for _ in range(n)],
                    direction="horizontal", gap=2, width="hug", node_id=E("S"))


SCREEN = dict(padding=fk.pad(14, 20, 20, 20), fill_=fk.fill("bg"), gap=20,
              safe_area=True, status_bar=True, scrollable=True,
              status_bar_theme="system")


# ============================================================== 1. hook
scr_hook = fk.screen(
    "scr_hook",
    [
        fk.stack([
            fk.text(fk.rich("HEADWAY"), preset="eyebrow", color_id="blue", node_id=E("T")),
            fk.text(fk.rich("The most successful people read. You don't have 8 hours."),
                    preset="h1", color_id="ink", node_id=E("T")),
            fk.text(fk.rich("Key ideas from 1,700+ bestsellers — 15 minutes each, "
                            "read or listened."),
                    preset="body", color_id="inkMid", node_id=E("T")),
        ], gap=10, node_id=E("S")),

        # Early proof for cold traffic. Every figure here is one Headway publishes.
        fk.stack([
            fk.stack([stars(), fk.text(fk.rich("4.6"), preset="rowT", color_id="ink",
                                       width="hug", node_id=E("T"))],
                     direction="horizontal", gap=6, align_v="center", width="hug",
                     node_id=E("S")),
            fk.text(fk.rich("150K+ App Store ratings · 50M+ readers"),
                    preset="small", color_id="inkMid", node_id=E("T")),
        ], gap=6, padding=fk.pad(14, 16, 16, 14), corner=fk.radius(16),
            fill_=fk.fill("card"), border="cardLine", node_id=E("S")),

        cta("Get started", "scr_method", sub="Takes about 60 seconds"),
    ],
    caption="Hook + early proof", progress_bar=False, **SCREEN)


# ============================================================== 2. method
def method_card(tag, a, b, c, tint, ink):
    return fk.stack([
        fk.text(fk.rich(tag), preset="badge", color_id=ink, node_id=E("T")),
        fk.text(fk.rich(a), preset="h3", color_id="ink", node_id=E("T")),
        fk.text(fk.rich(b), preset="small", color_id="inkMid", node_id=E("T")),
        fk.text(fk.rich(c), preset="small", color_id="inkMid", node_id=E("T")),
    ], gap=4, width="fill", padding=fk.pad(14, 14, 14, 14), corner=fk.radius(16),
        fill_=fk.fill(tint), border="cardLine", node_id=E("S"))


scr_method = fk.screen(
    "scr_method",
    [
        title_block(None, "One book. Fifteen minutes.",
                    "We read it, pull out the ideas that actually change how you work, "
                    "and hand you those."),
        fk.stack([
            method_card("A TYPICAL BOOK", "300+ pages", "8–10 hours", "Read only",
                        "card", "inkSoft"),
            method_card("ON HEADWAY", "Key ideas", "15 minutes", "Read or listen",
                        "blueSoft", "blue"),
        ], direction="horizontal", gap=12, node_id=E("S")),
        fk.stack([
            bullet("ListChecks", "Nothing padded",
                   "No anecdotes you already know, no filler chapters."),
            bullet("Lightning", "Built to stick",
                   "Key points first, then how to use them this week."),
        ], gap=14, node_id=E("S")),
        cta("Continue", "scr_goal"),
    ],
    caption="The method", progress_bar=False, **SCREEN)


# ============================================================== 3. goal  (single_choice)
# single_choice, NOT multi: a multi_choice group's selectedOptionId cannot be read by a
# conditional (it fails the publish gate), and every personalized line downstream reads
# this one. One primary goal also makes the paywall headline sharper.
GOALS = [
    ("career",     "Get ahead at work",        "Leadership, negotiation, strategy"),
    ("money",      "Build wealth",             "Money habits, investing, business"),
    ("confidence", "Be more confident",        "Self-belief, boundaries, resilience"),
    ("focus",      "Focus and get more done",  "Deep work, habits, procrastination"),
    ("people",     "Understand people better", "Communication, influence, relationships"),
]

scr_goal = mount_globals(fk.screen(
    "scr_goal",
    [
        pb_slot(),
        title_block(None, "What do you want to change first?",
                    "Pick one. Everything after this is built around it."),
        fk.stack([choice("goal", cid, lbl, sub) for cid, lbl, sub in GOALS],
                 gap=10, node_id=E("S")),
        cta("Continue", "scr_obstacle"),
    ],
    caption="Primary goal",
    selectable_groups=[{"id": "goal", "type": "single_choice"}],
    progress_bar=True, **SCREEN))


# ============================================================== 4. obstacle
OBSTACLES = [
    ("finish", "I start books and never finish them"),
    ("time",   "I can't find the time"),
    ("pick",   "I never know what to read next"),
    ("recall", "I read, but I don't remember any of it"),
]

scr_obstacle = mount_globals(fk.screen(
    "scr_obstacle",
    [
        pb_slot(),
        title_block(None, "What's gotten in the way?",
                    "Be honest — this changes what we put in front of you."),
        fk.stack([choice("obstacle", cid, lbl) for cid, lbl in OBSTACLES],
                 gap=10, node_id=E("S")),
        cta("Continue", "scr_pace"),
    ],
    caption="The obstacle",
    selectable_groups=[{"id": "obstacle", "type": "single_choice"}],
    progress_bar=True, **SCREEN))


# ============================================================== 5. pace
# The sub-lines are arithmetic on Headway's own "15 minutes per summary", not invented stats.
PACES = [
    ("m5",  "5 minutes",    "About 2 summaries a week"),
    ("m10", "10 minutes",   "A summary every other day"),
    ("m15", "15 minutes",   "A summary a day", True),
    ("m20", "20+ minutes",  "Two summaries a day"),
]

scr_pace = mount_globals(fk.screen(
    "scr_pace",
    [
        pb_slot(),
        title_block(None, "How much time can you give it a day?",
                    "Pick something you'd still do on a bad day."),
        fk.stack([choice("pace", p[0], p[1], p[2], default=len(p) > 3) for p in PACES],
                 gap=10, node_id=E("S")),
        cta("Continue", "scr_titles"),
    ],
    caption="Daily pace",
    selectable_groups=[{"id": "pace", "type": "single_choice"}],
    progress_bar=True, **SCREEN))


# ============================================================== 6. titles (multi_choice)
TITLES = [
    ("atomic",  "Atomic Habits",              "Tiny changes, remarkable results"),
    ("richdad", "Rich Dad Poor Dad",          "What the rich teach their kids about money"),
    ("deep",    "Deep Work",                  "Focused success in a distracted world"),
    ("talk",    "How to Talk to Anyone",      "92 little tricks for big success"),
    ("split",   "Never Split the Difference", "Negotiating as if your life depended on it"),
    ("club",    "The 5AM Club",               "Own your morning, elevate your life"),
]

scr_titles = mount_globals(fk.screen(
    "scr_titles",
    [
        pb_slot(),
        title_block(None, "Pick 3 to start with",
                    "They'll be waiting in your library when you're done here."),
        fk.stack([choice("titles", cid, lbl, sub) for cid, lbl, sub in TITLES],
                 gap=10, node_id=E("S")),
        cta("Continue", "scr_building"),
    ],
    caption="Pick your first titles",
    selectable_groups=[{"id": "titles", "type": "multi_choice"}],
    progress_bar=True, **SCREEN))


# ============================================================== 7. building (auto-advance)
# The device-verified auto-advance shape: a `timer` that is a direct child of root,
# absolute at 0,0, hug + padding, AND carrying at least one child. A childless timer does
# not fire on a device and the flow stops dead here — which is exactly what the seed flow
# in this app does. The seconds digit is a TEMPORARY diagnostic (see the handover note).
scr_building = fk.screen(
    "scr_building",
    [
        fk.stack([
            fk.text(fk.rich("Building your plan"), preset="h2", color_id="ink",
                    align="center", node_id=E("T")),
            fk.text(fk.rich("Matching summaries to your goal and the time you have."),
                    preset="body", color_id="inkMid", align="center", node_id=E("T")),
            loader_el(2900),
        ], gap=12, width="fill", padding=fk.pad(80, 8, 8, 24), align_h="center",
            node_id=E("S")),

        fk.stack([
            bullet("Check", "Goal locked in", tint="greenSoft", glyph="green"),
            bullet("Check", "Growth areas mapped", tint="greenSoft", glyph="green"),
            bullet("Check", "First summaries picked", tint="greenSoft", glyph="green"),
        ], gap=14, padding=fk.pad(16, 16, 16, 16), corner=fk.radius(16),
            fill_=fk.fill("card"), border="cardLine", node_id=E("S")),

        fk.timer(
            [fk.text(fk.rich("Headway"), preset="eyebrow", color_id="inkSoft",
                     width="hug", node_id=E("T")),
             fk.text(fk.rich("  \u00b7  "), preset="eyebrow", color_id="inkSoft",
                     width="hug", node_id=E("T")),
             fk.timer_digits(("seconds",), preset="eyebrow", color_id="inkSoft",
                             node_id=E("T"))],
            custom_id="build_delay", seconds=3,
            padding=fk.pad(12, 16, 16, 12),
            position=fk.absolute(top=0, left=0),
            actions=[fk.navigate("scr_plan")],
            caption="Auto-advance (3s) — the seconds digit is a temporary diagnostic",
            node_id=E("Timer")),
    ],
    caption="Building your plan", progress_bar=False,
    **{**SCREEN, "gap": 18})


# ============================================================== 8. plan (the payoff)
# The personalization loop is paid here, by echoing what the user actually chose. The flow
# can echo an answer; it cannot compute a projection, so nothing here is a modelled outcome.
GOAL_TITLE = fk.switch_rich(
    [(fk.eq(fk.ref("goal.selectedOptionId"), "career"),
      ["Your plan to ", fk.Span("get ahead at work", color="blue")]),
     (fk.eq(fk.ref("goal.selectedOptionId"), "money"),
      ["Your plan to ", fk.Span("build wealth", color="blue")]),
     (fk.eq(fk.ref("goal.selectedOptionId"), "confidence"),
      ["Your plan to ", fk.Span("be more confident", color="blue")]),
     (fk.eq(fk.ref("goal.selectedOptionId"), "focus"),
      ["Your plan to ", fk.Span("focus and get more done", color="blue")]),
     (fk.eq(fk.ref("goal.selectedOptionId"), "people"),
      ["Your plan to ", fk.Span("understand people better", color="blue")])],
    default=["Your reading plan"])

PACE_LINE = fk.switch_rich(
    [(fk.eq(fk.ref("pace.selectedOptionId"), "m5"),
      ["5 minutes a day — about 2 summaries a week"]),
     (fk.eq(fk.ref("pace.selectedOptionId"), "m10"),
      ["10 minutes a day — a summary every other day"]),
     (fk.eq(fk.ref("pace.selectedOptionId"), "m15"),
      ["15 minutes a day — a summary a day"]),
     (fk.eq(fk.ref("pace.selectedOptionId"), "m20"),
      ["20+ minutes a day — two summaries a day"])],
    default=["The pace you picked"])

OBSTACLE_LINE = fk.switch_rich(
    [(fk.eq(fk.ref("obstacle.selectedOptionId"), "finish"),
      ["Short enough to finish — that was the thing stopping you"]),
     (fk.eq(fk.ref("obstacle.selectedOptionId"), "time"),
      ["Sized to the time you actually have, not the time you wish you had"]),
     (fk.eq(fk.ref("obstacle.selectedOptionId"), "pick"),
      ["Picked for you, so you never stall on what to read next"]),
     (fk.eq(fk.ref("obstacle.selectedOptionId"), "recall"),
      ["Key points up front, so it stays with you after you close the app"])],
    default=["Built around what gets in your way"])


def payoff_row(icon_name, content):
    return fk.stack([
        fk.stack([fk.icon(icon_name, size_pt=16, color_id="blue", weight=IW[icon_name],
                          node_id=E("I"))],
                 fixed_w=32, fixed_h=32, corner=fk.radius(16), fill_=fk.fill("blueSoft"),
                 align_h="center", align_v="center", node_id=E("S")),
        fk.text(content, preset="rowT", color_id="ink", node_id=E("T")),
    ], direction="horizontal", gap=12, align_v="center", node_id=E("S"))


scr_plan = fk.screen(
    "scr_plan",
    [
        fk.stack([
            fk.text(fk.rich("YOUR PLAN IS READY"), preset="eyebrow", color_id="green",
                    node_id=E("T")),
            fk.text(GOAL_TITLE, preset="h1", color_id="ink", node_id=E("T")),
        ], gap=8, node_id=E("S")),

        fk.stack([
            payoff_row("Lightning", PACE_LINE),
            payoff_row("ListChecks", OBSTACLE_LINE),
            payoff_row("Heart", fk.rich("The titles you picked are saved to your library")),
        ], gap=16, padding=fk.pad(18, 16, 16, 18), corner=fk.radius(18),
            fill_=fk.fill("card"), border="cardLine", node_id=E("S")),

        fk.text(fk.rich("You can change any of this later — the plan moves with you."),
                preset="small", color_id="inkSoft", node_id=E("T")),

        cta("Continue", "scr_pact"),
    ],
    caption="Personalized plan (the payoff)", progress_bar=False, **SCREEN)


# ============================================================== 9. commitment pact
PACT_PLEDGE = fk.switch_rich(
    [(fk.eq(fk.ref("pace.selectedOptionId"), "m5"),
      ["I'll give this ", fk.Span("5 minutes a day", bold=True), "."]),
     (fk.eq(fk.ref("pace.selectedOptionId"), "m10"),
      ["I'll give this ", fk.Span("10 minutes a day", bold=True), "."]),
     (fk.eq(fk.ref("pace.selectedOptionId"), "m15"),
      ["I'll give this ", fk.Span("15 minutes a day", bold=True), "."]),
     (fk.eq(fk.ref("pace.selectedOptionId"), "m20"),
      ["I'll give this ", fk.Span("20 minutes a day", bold=True), "."])],
    default=["I'll give this a few minutes a day."])

scr_pact = fk.screen(
    "scr_pact",
    [
        title_block("ONE LAST THING", "Your commitment",
                    "People who commit out loud are far more likely to keep going. "
                    "It takes one tap."),
        fk.stack([
            fk.stack([fk.icon("Sparkle", size_pt=22, color_id="blue", weight=IW["Sparkle"],
                              node_id=E("I"))],
                     fixed_w=44, fixed_h=44, corner=fk.radius(22),
                     fill_=fk.fill("blueSoft"), align_h="center", align_v="center",
                     node_id=E("S")),
            fk.text(PACT_PLEDGE, preset="h3", color_id="ink", node_id=E("T")),
            fk.text(fk.rich("I'll finish what I start, and I'll let Headway pick the "
                            "next one so I don't stall."),
                    preset="body", color_id="inkMid", node_id=E("T")),
        ], gap=12, padding=fk.pad(20, 18, 18, 20), corner=fk.radius(18),
            fill_=fk.fill("card"), border="cardLine", node_id=E("S")),

        cta("I commit", "scr_paywall", sub="No payment involved — this is just a promise "
                                           "to yourself"),
    ],
    caption="Commitment pact", progress_bar=False, **SCREEN)


# ============================================================== 10. paywall
PW_TITLE = fk.switch_rich(
    [(fk.eq(fk.ref("goal.selectedOptionId"), "career"),
      ["Unlock your plan to ", fk.Span("get ahead at work", color="blue")]),
     (fk.eq(fk.ref("goal.selectedOptionId"), "money"),
      ["Unlock your plan to ", fk.Span("build wealth", color="blue")]),
     (fk.eq(fk.ref("goal.selectedOptionId"), "confidence"),
      ["Unlock your plan to ", fk.Span("be more confident", color="blue")]),
     (fk.eq(fk.ref("goal.selectedOptionId"), "focus"),
      ["Unlock your plan to ", fk.Span("focus and get more done", color="blue")]),
     (fk.eq(fk.ref("goal.selectedOptionId"), "people"),
      ["Unlock your plan to ", fk.Span("understand people better", color="blue")])],
    default=["Unlock your reading plan"])


def plan_card(product_id, name, price_var, sub_parts, *, default=False, badge=None):
    left = [fk.on_selected(fk.text(fk.rich(name), preset="plan", color_id="ink",
                                   node_id=E("T")),
                           color=fk.color("blue"))]
    left.append(fk.text(fk.rich(*sub_parts), preset="planSub", color_id="inkMid",
                        node_id=E("T")))

    head = [fk.stack(left, gap=3, width="fill", node_id=E("S"))]
    if badge:
        head.append(fk.stack(
            [fk.text(fk.rich(badge), preset="badge", color_id="onAmber", align="center",
                     width="hug", node_id=E("T"))],
            width="hug", padding=fk.pad(5, 9, 9, 5), corner=fk.radius(9),
            fill_=fk.fill("amber"), align_h="center", align_v="center", node_id=E("S")))

    return fk.on_selected(
        fk.product([
            fk.stack(head, direction="horizontal", gap=8, align_v="center", width="fill",
                     node_id=E("S")),
            fk.text(fk.rich(fk.Var(price_var)), preset="price", color_id="ink",
                    node_id=E("T")),
        ], product_id=product_id, group_id="plans", default=default,
            width="fill", gap=6, padding=fk.pad(15, 16, 16, 15), corner=fk.radius(16),
            fill_=fk.fill("card"), border="cardLine", node_id=E("S")),
        fill=fk.fill("blueSoft"),
        border={"color": fk.color("blue"), "style": "solid", "width": 1},
        padding=fk.pad(15, 16, 16, 15), borderRadius=fk.radius(16))


scr_paywall = fk.screen(
    "scr_paywall",
    [
        # Close is an X, not a buried "view other plans" link — both plans are already here.
        fk.stack([
            fk.stack([], width="fill", node_id=E("S")),
            fk.stack([fk.icon("X", size_pt=17, color_id="inkSoft", weight=IW["X"], node_id=E("I"))],
                     fixed_w=32, fixed_h=32, corner=fk.radius(16), fill_=fk.fill("card"),
                     align_h="center", align_v="center",
                     actions=[fk.close()], node_id=E("S")),
        ], direction="horizontal", width="fill", align_v="center", node_id=E("S")),

        fk.text(PW_TITLE, preset="h2", color_id="ink", node_id=E("T")),

        fk.stack([
            bullet("ListChecks", "1,700+ summaries", "15 minutes each, new titles weekly"),
            bullet("Lightning", "Read or listen", "On the commute, the walk, the queue"),
            bullet("Check", "Your plan, kept up to date",
                   "Picks change as your goal does — and streaks keep it alive",
                   tint="greenSoft", glyph="green"),
        ], gap=13, node_id=E("S")),

        # Proof at the decision point. One real, verbatim App Store review — a second card
        # would need a second real quote, and an invented one is a fabricated proof number
        # wearing a person's name. See the handover note.
        fk.stack([
            fk.stack([stars(), fk.text(fk.rich("4.6 · 150K+ ratings"), preset="small",
                                       color_id="inkMid", width="hug", node_id=E("T"))],
                     direction="horizontal", gap=8, align_v="center", node_id=E("S")),
            fk.text(fk.rich("“I never have time to read a full book and often feel "
                            "frustrated by that. These summaries have been helpful.”"),
                    preset="body", color_id="ink", node_id=E("T")),
            fk.text(fk.rich("Susan O'Neill · App Store"), preset="small",
                    color_id="inkSoft", node_id=E("T")),
        ], gap=6, padding=fk.pad(12, 14, 14, 12), corner=fk.radius(16),
            fill_=fk.fill("quote"), border="cardLine", node_id=E("S")),

        # Both plans visible. The per-month figure on the annual card is derived by the SDK
        # from the real store price — that is the savings visualization, with no invented %.
        fk.stack([
            plan_card(YEAR, "12 months",
                      f"{YEAR}.prod_price",
                      [fk.Var(f"{YEAR}.prod_price_per_month"), " per month, billed yearly"],
                      default=True, badge="BEST VALUE"),
            plan_card(MONTH, "1 month",
                      f"{MONTH}.prod_price",
                      ["Billed monthly, cancel whenever"]),
        ], gap=10, node_id=E("S")),

        fk.footer([
            fk.stack([fk.text(fk.rich("Start reading"), preset="btn", color_id="onBlue",
                              align="center", node_id=E("T"))],
                     width="fill", fixed_h=56, corner=fk.radius(28),
                     fill_=fk.fill("blue"), align_h="center", align_v="center",
                     actions=[fk.purchase("plans")], node_id=E("S")),
            fk.text(fk.rich("Cancel anytime in the App Store."), preset="small",
                    color_id="inkMid", align="center", node_id=E("T")),
            fk.stack([
                fk.text(fk.rich("Terms"), preset="legal", color_id="inkSoft", width="hug",
                        align="center",
                        actions=[fk.open_url("https://headway.app/terms", external=True,
                                             action_id="act_terms")], node_id=E("T")),
                fk.text(fk.rich("Privacy"), preset="legal", color_id="inkSoft", width="hug",
                        align="center",
                        actions=[fk.open_url("https://headway.app/privacy", external=True,
                                             action_id="act_privacy")], node_id=E("T")),
                fk.text(fk.rich("Restore"), preset="legal", color_id="inkSoft", width="hug",
                        align="center",
                        actions=[fk.restore()], node_id=E("T")),
            ], direction="horizontal", gap=18, align_h="center", width="fill",
                node_id=E("S")),
        ], fill_=fk.fill("bg"), padding=fk.pad(10, 20, 20, 20), gap=10, node_id=E("S")),
    ],
    caption="Paywall — goal-personalized",
    selectable_groups=[{"id": "plans", "type": "product"}],
    progress_bar=False,
    **{**SCREEN, "padding": fk.pad(8, 20, 20, 20), "gap": 12})


# ============================================================== assemble
cfg = fk.config(
    screens=[scr_hook, scr_method, scr_goal, scr_obstacle, scr_pace, scr_titles,
             scr_building, scr_plan, scr_pact, scr_paywall],
    colors=[(i, n, hx, hx) for i, n, hx in COLORS],  # dark mirrors light: one light system
    typography=TYPO,
    icons=ICONS,
    components=PROGRESS,
    meta_screens=fk.predeclare("scr_paywall", [YEAR, MONTH]),
)
cfg["schemaVersion"] = 11


# A price variable node in a real export carries `productRef` alongside `variableId`.
# flowkit emits the bare id; match the shape the live flow in this app renders with.
def add_product_refs(node):
    if isinstance(node, dict):
        if node.get("type") == "variable":
            attrs = node.get("attrs") or {}
            vid = attrs.get("variableId", "")
            if "." in vid and vid.split(".", 1)[1].startswith("prod_"):
                pid, field = vid.split(".", 1)
                attrs["productRef"] = {"field": field,
                                       "target": {"id": pid, "kind": "product"}}
        for v in node.values():
            add_product_refs(v)
    elif isinstance(node, list):
        for v in node:
            add_product_refs(v)


add_product_refs(cfg)

out = HERE / "draft.json"
out.write_text(json.dumps(cfg, indent=1))
n_el = sum(len(s["elements"]["map"]) for s in cfg["screens"])
print(f"wrote {out}  screens={len(cfg['screens'])}  elements={n_el}")
