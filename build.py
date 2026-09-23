#!/usr/bin/env python3
"""Headway — Onboarding + Paywall (CR rebuild).

Skeleton: personalization loop (goal -> quiz -> short loader -> echoed plan) with a
commitment beat at the seam. Grounded in the ScreensDesign replay of Headway's live flow,
with the contradiction rules applied: no sign-up wall, no permission prompts before the
paywall, every captured answer consumed, and the paywall headline naming the user's goal.

Design system — "paper & ink, with a marigold spark":
  * warm paper page, near-black warm ink, ONE saturated accent. No second hue competing.
  * full-bleed ink hero blocks instead of cards floating on a tint.
  * the typographic scale does the work: 44pt numerals against 11pt tracked labels.
  * the selected state INVERTS (ink fill, paper text) rather than tinting — unmissable, and
    it changes no geometry, so nothing reflows on tap.
  * the paywall goes dark. Nine light screens precede it, so the money moment reads as
    arriving somewhere rather than as one more card.
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
    ("paper",    "Paper",             "#FAF5EE"),
    ("card",     "Card",              "#FFFFFF"),
    ("line",     "Hairline",          "#E7DCCC"),
    ("ink",      "Ink",               "#191512"),
    ("inkMid",   "Ink mid",           "#6A6055"),
    ("inkSoft",  "Ink soft",          "#9C9184"),
    ("onInk",    "On ink",            "#FAF5EE"),
    ("onInkMid", "On ink mid",        "#B4A898"),
    ("mari",     "Marigold",          "#E07A28"),
    ("mariDeep", "Marigold deep",     "#B75F19"),
    ("mariSoft", "Marigold tint",     "#FBE9D7"),
    ("green",    "Green",             "#2F7A5B"),
    ("greenSoft", "Green tint",       "#E2F0E9"),
    # paywall surfaces
    ("dkBg",     "Paywall ink",       "#17130F"),
    ("dkCard",   "Paywall card",      "#241E18"),
    ("dkLine",   "Paywall line",      "#3A322A"),
    ("dkOn",     "Paywall selected",  "#2E2317"),
    ("dkMid",    "Paywall ink mid",   "#A89C8C"),
    ("dkSoft",   "Paywall ink soft",  "#7C7264"),
]

TYPO = [
    # id, name, size, weight, lineHeight, letterSpacing
    ("eyebrow", "Eyebrow",        11, "bold",     14, 1.6),
    ("display", "Display",        34, "bold",     38, -0.4),
    ("h1",      "Screen title",   27, "bold",     32, -0.2),
    ("h2",      "Section title",  22, "bold",     27, None),
    ("h3",      "Card title",     18, "bold",     23, None),
    ("num",     "Big numeral",    44, "bold",     46, -1.2),
    ("rowT",    "Row title",      16, "semibold", 21, None),
    ("body",    "Body",           15, "regular",  22, None),
    ("small",   "Small",          13, "regular",  18, None),
    ("legal",   "Legal",          11, "regular",  15, None),
    ("btn",     "Button",         17, "bold",     21, None),
    ("plan",    "Plan name",      17, "bold",     22, None),
    ("planSub", "Plan sub",       13, "regular",  17, None),
    ("price",   "Price",          21, "bold",     25, None),
    ("badge",   "Badge",          10, "bold",     13, 0.9),
]

# Real Phosphor SVG lifted from CampRoute Pro in the same app — never fabricated markup.
ICONS = json.loads((HERE / "icons.json").read_text())
# (name, weight) must match an entry in _meta.icons exactly, or the publish gate refuses it.
IW = {i["name"]: i["weight"] for i in ICONS}


# ------------------------------------------------------------------ progress bar
# A real progress-bar component wired through props.progressBar — not a row of decorative
# stacks, which renders identically in a screenshot and never advances.
PB_ID = "pb_dots"
PROGRESS = {PB_ID: {
    "map": {
        "el_pbBar": {"id": "el_pbBar", "type": "progress-bar", "states": [], "props": {
            "type": "multiple-segments", "template": "dots", "oneSegmentPerScreen": True,
            "width": fk.size("hug"), "height": fk.size("fixed", 4),
            "layout": fk.layout("horizontal", 6, "center", "center"),
            "position": fk.relative()}},
        "el_pbSeg": {"id": "el_pbSeg", "type": "progress-bar-segment", "states": [], "props": {
            "customId": "progress",
            "fill": fk.fill("line"),
            "width": fk.size("fixed", 24), "height": fk.size("fixed", 4),
            "borderRadius": fk.radius(2)}},
        "el_pbLoad": {"id": "el_pbLoad", "type": "progress-bar-loader", "states": [], "props": {
            "fill": fk.fill("mari"), "color": fk.color("mari"),
            "easing": "ease-in-out", "duration": 320,
            "position": fk.relative(), "borderRadius": fk.radius(2)}},
    },
    "hierarchy": {"id": "root", "children": [
        {"id": "el_pbBar", "children": [
            {"id": "el_pbSeg", "children": [{"id": "el_pbLoad"}]}]}]}}}


def loader_el(duration_ms):
    """The real determinate `loader` element. A static filled stack looks identical in a
    screenshot and never advances — the fake-progress-bar shape patterns.md forbids."""
    return {"id": E("S"), "type": "loader", "states": [], "caption": "Progress",
            "props": {"fill": fk.fill("line"), "color": fk.color("mari"),
                      "width": fk.size("fill"), "height": fk.size("fixed", 5),
                      "easing": "linear", "duration": duration_ms,
                      "position": fk.relative(), "borderRadius": fk.radius(3)}}


# A component is referenced from a screen hierarchy as a node with NO entry in that screen's
# map — flowkit's flatten() has no notion of that, so the slot is built as a marker stack and
# swapped for the `global` node after the screen is assembled.
_MARKERS = set()


def pb_slot():
    mid = E("S")
    _MARKERS.add(mid)
    return fk.stack([fk.stack([], node_id=mid)], width="hug", align_h="start",
                    node_id=E("S"))


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
def cta(label, target=None, *, actions=None, sub=None, page="paper",
        btn_fill="ink", btn_ink="onInk", sub_ink="inkSoft"):
    """The pinned bottom bar: one full-width primary button, optional line under it."""
    button = fk.stack(
        [fk.stack([
            fk.text(fk.rich(label), preset="btn", color_id=btn_ink, align="center",
                    width="hug", node_id=E("T")),
            fk.icon("ArrowRight", size_pt=17, color_id=btn_ink, weight=IW["ArrowRight"],
                    node_id=E("I")),
        ], direction="horizontal", gap=9, align_h="center", align_v="center",
            width="hug", node_id=E("S"))],
        width="fill", fixed_h=58, corner=fk.radius(16), fill_=fk.fill(btn_fill),
        align_h="center", align_v="center",
        actions=actions if actions is not None else [fk.navigate(target)],
        node_id=E("S"))
    kids = [button]
    if sub:
        kids.append(fk.text(fk.rich(sub), preset="small", color_id=sub_ink,
                            align="center", node_id=E("T")))
    return fk.footer(kids, fill_=fk.fill(page), padding=fk.pad(12, 20, 24, 20),
                     gap=10, node_id=E("S"))


def hero(eyebrow, title_parts, sub=None, *, pad_top=56):
    """A full-bleed ink block. Rounded only at the bottom, so it reads as printed stock
    rather than as a card someone dropped on the page."""
    # `title_parts` is either rich-text parts, or an already-built localizable (a switch).
    title = title_parts if isinstance(title_parts, dict) else fk.rich(*title_parts)
    kids = [fk.text(fk.rich(eyebrow), preset="eyebrow", color_id="mari", node_id=E("T")),
            fk.text(title, preset="display", color_id="onInk", node_id=E("T"))]
    if sub:
        kids.append(fk.text(fk.rich(sub), preset="body", color_id="onInkMid",
                            node_id=E("T")))
    return fk.stack(kids, gap=14, width="fill", fill_=fk.fill("ink"),
                    padding=fk.pad(pad_top, 22, 22, 34),
                    corner=fk.radius(tl=0, tr=0, bl=30, br=30), node_id=E("S"))


def step_head(step, title, sub=None):
    """Step counter and the progress dots share one line above the question."""
    return fk.stack([
        fk.stack([
            fk.text(fk.rich(step), preset="eyebrow", color_id="mari", width="hug",
                    node_id=E("T")),
            pb_slot(),
        ], direction="horizontal", gap=12, align_v="center", width="fill", node_id=E("S")),
        fk.text(fk.rich(title), preset="h1", color_id="ink", node_id=E("T")),
    ] + ([fk.text(fk.rich(sub), preset="body", color_id="inkMid", node_id=E("T"))]
         if sub else []),
        gap=10, node_id=E("S"))


def choice(group, custom_id, label, sub=None, default=False):
    """One quiz option. Identical base look on every card; selected INVERTS to ink.

    Only fill and colour change between states — a border-width or padding delta would
    resize the card and reflow every sibling in a fill-width column.
    """
    kids = [fk.on_selected(
        fk.text(fk.rich(label), preset="rowT", color_id="ink", node_id=E("T")),
        color=fk.color("onInk"))]
    if sub:
        kids.append(fk.on_selected(
            fk.text(fk.rich(sub), preset="small", color_id="inkSoft", node_id=E("T")),
            color=fk.color("mari")))
    return fk.on_selected(
        fk.selectable([fk.stack(kids, gap=3, node_id=E("S"))],
                      group_id=group, custom_id=custom_id, default=default,
                      width="fill", padding=fk.pad(16, 18, 18, 16),
                      corner=fk.radius(14), fill_=fk.fill("card"),
                      border="line", align_v="center", node_id=E("S")),
        fill=fk.fill("ink"),
        border={"color": fk.color("ink"), "style": "solid", "width": 1},
        padding=fk.pad(16, 18, 18, 16), borderRadius=fk.radius(14))


def bullet(icon_name, label, sub=None, *, tint="mariSoft", glyph="mariDeep",
           ink="ink", ink_sub="inkMid"):
    text_kids = [fk.text(fk.rich(label), preset="rowT", color_id=ink, node_id=E("T"))]
    if sub:
        text_kids.append(fk.text(fk.rich(sub), preset="small", color_id=ink_sub,
                                 node_id=E("T")))
    return fk.stack([
        fk.stack([fk.icon(icon_name, size_pt=15, color_id=glyph, weight=IW[icon_name],
                          node_id=E("I"))],
                 fixed_w=30, fixed_h=30, corner=fk.radius(10), fill_=fk.fill(tint),
                 align_h="center", align_v="center", node_id=E("S")),
        fk.stack(text_kids, gap=2, node_id=E("S")),
    ], direction="horizontal", gap=13, align_v="center", node_id=E("S"))


def rule(color_id="line"):
    return fk.stack([], width="fill", fixed_h=1, fill_=fk.fill(color_id), node_id=E("S"))


def stars(size_pt=13, color_id="mari"):
    return fk.stack([fk.icon("Star", size_pt=size_pt, color_id=color_id,
                             weight=IW["Star"], node_id=E("I")) for _ in range(5)],
                    direction="horizontal", gap=2, width="hug", node_id=E("S"))


def body_pad(children, gap=20, pad=(20, 20, 20, 0)):
    return fk.stack(children, gap=gap, width="fill", padding=fk.pad(*pad), node_id=E("S"))


# Screens are edge-to-edge; each block owns its padding, so a hero can bleed to the edges.
SCREEN = dict(padding=fk.pad(0, 0, 0, 12), fill_=fk.fill("paper"), gap=18,
              safe_area=True, status_bar=True, scrollable=True,
              status_bar_theme="system")
QUIZ = {**SCREEN, "padding": fk.pad(14, 0, 0, 12), "gap": 22}


# ============================================================== 1. hook
scr_hook = fk.screen(
    "scr_hook",
    [
        hero("HEADWAY",
             ["The most successful people read.\n",
              fk.Span("You don't have 8 hours.", color="mari")],
             "Key ideas from 1,700+ bestsellers — fifteen minutes each, read or listened."),

        body_pad([
            fk.stack([
                stars(),
                fk.text(fk.rich("4.6"), preset="rowT", color_id="ink", width="hug",
                        node_id=E("T")),
            ], direction="horizontal", gap=7, align_v="center", width="hug",
                node_id=E("S")),
            fk.text(fk.rich("150K+ App Store ratings · 50M+ readers"),
                    preset="small", color_id="inkMid", node_id=E("T")),
        ], gap=7, pad=(22, 22, 22, 0)),

        cta("Get started", "scr_method", sub="Takes about 60 seconds"),
    ],
    caption="Hook + early proof", progress_bar=False, **SCREEN)


# ============================================================== 2. method
def num_tile(numeral, unit, a, b, *, dark=False):
    return fk.stack([
        fk.text(fk.rich(numeral), preset="num", color_id="mari" if dark else "ink",
                node_id=E("T")),
        fk.text(fk.rich(unit), preset="eyebrow",
                color_id="onInkMid" if dark else "inkSoft", node_id=E("T")),
        rule("dkLine" if dark else "line"),
        fk.text(fk.rich(a), preset="small", color_id="onInk" if dark else "inkMid",
                node_id=E("T")),
        fk.text(fk.rich(b), preset="small", color_id="onInkMid" if dark else "inkSoft",
                node_id=E("T")),
    ], gap=7, width="fill", padding=fk.pad(18, 16, 16, 18), corner=fk.radius(18),
        fill_=fk.fill("ink" if dark else "card"),
        border=None if dark else "line", node_id=E("S"))


scr_method = fk.screen(
    "scr_method",
    [
        body_pad([
            fk.stack([
                fk.text(fk.rich("THE TRADE"), preset="eyebrow", color_id="mari",
                        node_id=E("T")),
                fk.text(fk.rich("One book.\nFifteen minutes."), preset="display",
                        color_id="ink", node_id=E("T")),
                fk.text(fk.rich("We read it, pull out the ideas that actually change how "
                                "you work, and hand you those."),
                        preset="body", color_id="inkMid", node_id=E("T")),
            ], gap=12, node_id=E("S")),

            fk.stack([
                num_tile("300+", "PAGES", "8–10 hours", "Read only"),
                num_tile("15", "MINUTES", "Key ideas first", "Read or listen", dark=True),
            ], direction="horizontal", gap=12, node_id=E("S")),

            fk.stack([
                bullet("ListChecks", "Nothing padded",
                       "No anecdotes you already know, no filler chapters."),
                bullet("Lightning", "Built to stick",
                       "Key points first, then how to use them this week."),
            ], gap=16, node_id=E("S")),
        ], gap=22, pad=(18, 20, 20, 0)),

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
        body_pad([
            step_head("01 / 04", "What do you want to change first?",
                      "Pick one. Everything after this is built around it."),
            fk.stack([choice("goal", cid, lbl, sub) for cid, lbl, sub in GOALS],
                     gap=10, node_id=E("S")),
        ], gap=22),
        cta("Continue", "scr_obstacle"),
    ],
    caption="Primary goal",
    selectable_groups=[{"id": "goal", "type": "single_choice"}],
    progress_bar=True, **QUIZ))


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
        body_pad([
            step_head("02 / 04", "What's gotten in the way?",
                      "Be honest — this changes what we put in front of you."),
            fk.stack([choice("obstacle", cid, lbl) for cid, lbl in OBSTACLES],
                     gap=10, node_id=E("S")),
        ], gap=22),
        cta("Continue", "scr_pace"),
    ],
    caption="The obstacle",
    selectable_groups=[{"id": "obstacle", "type": "single_choice"}],
    progress_bar=True, **QUIZ))


# ============================================================== 5. pace
# The sub-lines are arithmetic on Headway's own "15 minutes per summary", not invented stats.
PACES = [
    ("m5",  "5 minutes",   "About 2 summaries a week"),
    ("m10", "10 minutes",  "A summary every other day"),
    ("m15", "15 minutes",  "A summary a day", True),
    ("m20", "20+ minutes", "Two summaries a day"),
]

scr_pace = mount_globals(fk.screen(
    "scr_pace",
    [
        body_pad([
            step_head("03 / 04", "How much time can you give it a day?",
                      "Pick something you'd still do on a bad day."),
            fk.stack([choice("pace", p[0], p[1], p[2], default=len(p) > 3) for p in PACES],
                     gap=10, node_id=E("S")),
        ], gap=22),
        cta("Continue", "scr_titles"),
    ],
    caption="Daily pace",
    selectable_groups=[{"id": "pace", "type": "single_choice"}],
    progress_bar=True, **QUIZ))


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
        body_pad([
            step_head("04 / 04", "Pick 3 to start with",
                      "They'll be waiting in your library when you're done here."),
            fk.stack([choice("titles", cid, lbl, sub) for cid, lbl, sub in TITLES],
                     gap=10, node_id=E("S")),
        ], gap=22),
        cta("Continue", "scr_building"),
    ],
    caption="Pick your first titles",
    selectable_groups=[{"id": "titles", "type": "multi_choice"}],
    progress_bar=True, **QUIZ))


# ============================================================== 7. building (auto-advance)
# The device-verified auto-advance shape: a `timer` that is a direct child of root,
# absolute at 0,0, hug + padding, AND carrying at least one child. A childless timer does
# not fire on a device and the flow stops dead here. The seconds digit is a TEMPORARY
# diagnostic; the wordmark beside it is the child that must stay.
scr_building = fk.screen(
    "scr_building",
    [
        body_pad([
            fk.stack([
                fk.text(fk.rich("ONE MOMENT"), preset="eyebrow", color_id="mari",
                        align="center", node_id=E("T")),
                fk.text(fk.rich("Building your plan"), preset="h1", color_id="ink",
                        align="center", node_id=E("T")),
                fk.text(fk.rich("Matching summaries to your goal and the time you have."),
                        preset="body", color_id="inkMid", align="center", node_id=E("T")),
            ], gap=10, width="fill", align_h="center", node_id=E("S")),

            loader_el(2900),

            fk.stack([
                bullet("Check", "Goal locked in", tint="greenSoft", glyph="green"),
                bullet("Check", "Growth areas mapped", tint="greenSoft", glyph="green"),
                bullet("Check", "First summaries picked", tint="greenSoft", glyph="green"),
            ], gap=16, padding=fk.pad(18, 18, 18, 18), corner=fk.radius(18),
                fill_=fk.fill("card"), border="line", node_id=E("S")),
        ], gap=26, pad=(96, 20, 20, 0)),

        fk.timer(
            [fk.text(fk.rich("HEADWAY"), preset="eyebrow", color_id="inkSoft",
                     width="hug", node_id=E("T")),
             fk.text(fk.rich("  ·  "), preset="eyebrow", color_id="inkSoft",
                     width="hug", node_id=E("T")),
             fk.timer_digits(("seconds",), preset="eyebrow", color_id="inkSoft",
                             node_id=E("T"))],
            custom_id="build_delay", seconds=3,
            padding=fk.pad(14, 20, 20, 14),
            position=fk.absolute(top=0, left=0),
            actions=[fk.navigate("scr_plan")],
            caption="Auto-advance (3s) — the seconds digit is a temporary diagnostic",
            node_id=E("Timer")),
    ],
    caption="Building your plan", progress_bar=False, **SCREEN)


# ============================================================== 8. plan (the payoff)
# The personalization loop is paid here, by echoing what the user actually chose. The flow
# can echo an answer; it cannot compute a projection, so nothing here is a modelled outcome.
GOAL_WORDS = [
    ("career",     "get ahead at work"),
    ("money",      "build wealth"),
    ("confidence", "be more confident"),
    ("focus",      "focus and get more done"),
    ("people",     "understand people better"),
]

GOAL_TITLE = fk.switch_rich(
    [(fk.eq(fk.ref("goal.selectedOptionId"), cid),
      ["Your plan to\n", fk.Span(words, color="mari")]) for cid, words in GOAL_WORDS],
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
      ["Sized to the time you have, not the time you wish you had"]),
     (fk.eq(fk.ref("obstacle.selectedOptionId"), "pick"),
      ["Picked for you, so you never stall on what to read next"]),
     (fk.eq(fk.ref("obstacle.selectedOptionId"), "recall"),
      ["Key points up front, so it stays with you after you close the app"])],
    default=["Built around what gets in your way"])


def payoff_row(icon_name, content, *, last=False):
    row = fk.stack([
        fk.stack([fk.icon(icon_name, size_pt=15, color_id="mariDeep",
                          weight=IW[icon_name], node_id=E("I"))],
                 fixed_w=30, fixed_h=30, corner=fk.radius(10), fill_=fk.fill("mariSoft"),
                 align_h="center", align_v="center", node_id=E("S")),
        fk.text(content, preset="rowT", color_id="ink", node_id=E("T")),
    ], direction="horizontal", gap=13, align_v="center", node_id=E("S"))
    if last:
        return row
    return fk.stack([row, rule()], gap=15, node_id=E("S"))


scr_plan = fk.screen(
    "scr_plan",
    [
        hero("YOUR PLAN IS READY", GOAL_TITLE, pad_top=52),

        body_pad([
            fk.stack([
                payoff_row("Lightning", PACE_LINE),
                payoff_row("ListChecks", OBSTACLE_LINE),
                payoff_row("Heart",
                           fk.rich("The titles you picked are saved to your library"),
                           last=True),
            ], gap=15, padding=fk.pad(20, 18, 18, 20), corner=fk.radius(18),
                fill_=fk.fill("card"), border="line", node_id=E("S")),

            fk.text(fk.rich("You can change any of this later — the plan moves with you."),
                    preset="small", color_id="inkSoft", node_id=E("T")),
        ], gap=14, pad=(20, 20, 20, 0)),

        cta("Continue", "scr_pact"),
    ],
    caption="Personalized plan (the payoff)", progress_bar=False, **SCREEN)


# ============================================================== 9. commitment pact
PACT_PLEDGE = fk.switch_rich(
    [(fk.eq(fk.ref("pace.selectedOptionId"), "m5"),
      ["I'll give this ", fk.Span("5 minutes a day", color="mari"), "."]),
     (fk.eq(fk.ref("pace.selectedOptionId"), "m10"),
      ["I'll give this ", fk.Span("10 minutes a day", color="mari"), "."]),
     (fk.eq(fk.ref("pace.selectedOptionId"), "m15"),
      ["I'll give this ", fk.Span("15 minutes a day", color="mari"), "."]),
     (fk.eq(fk.ref("pace.selectedOptionId"), "m20"),
      ["I'll give this ", fk.Span("20 minutes a day", color="mari"), "."])],
    default=["I'll give this a few minutes a day."])

scr_pact = fk.screen(
    "scr_pact",
    [
        body_pad([
            fk.stack([
                fk.text(fk.rich("ONE LAST THING"), preset="eyebrow", color_id="mari",
                        node_id=E("T")),
                fk.text(fk.rich("Your commitment"), preset="display", color_id="ink",
                        node_id=E("T")),
                fk.text(fk.rich("People who commit out loud are far more likely to keep "
                                "going. It takes one tap."),
                        preset="body", color_id="inkMid", node_id=E("T")),
            ], gap=12, node_id=E("S")),

            # The pledge reads as something signed: ink card, their own number in accent.
            fk.stack([
                fk.stack([fk.icon("Sparkle", size_pt=20, color_id="ink",
                                  weight=IW["Sparkle"], node_id=E("I"))],
                         fixed_w=42, fixed_h=42, corner=fk.radius(21),
                         fill_=fk.fill("mari"), align_h="center", align_v="center",
                         node_id=E("S")),
                fk.text(PACT_PLEDGE, preset="h2", color_id="onInk", node_id=E("T")),
                rule("dkLine"),
                fk.text(fk.rich("I'll finish what I start, and I'll let Headway pick the "
                                "next one so I don't stall."),
                        preset="body", color_id="onInkMid", node_id=E("T")),
            ], gap=16, padding=fk.pad(24, 22, 22, 24), corner=fk.radius(20),
                fill_=fk.fill("ink"), node_id=E("S")),
        ], gap=24, pad=(24, 20, 20, 0)),

        cta("I commit", "scr_paywall",
            sub="No payment involved — this is just a promise to yourself"),
    ],
    caption="Commitment pact", progress_bar=False, **SCREEN)


# ============================================================== 10. paywall (dark)
PW_TITLE = fk.switch_rich(
    [(fk.eq(fk.ref("goal.selectedOptionId"), cid),
      ["Unlock your plan to ", fk.Span(words, color="mari")]) for cid, words in GOAL_WORDS],
    default=["Unlock your reading plan"])


def plan_card(product_id, name, price_var, sub_parts, *, default=False, badge=None):
    head = [fk.stack([
        fk.on_selected(fk.text(fk.rich(name), preset="plan", color_id="onInk",
                               node_id=E("T")),
                       color=fk.color("mari")),
        fk.text(fk.rich(*sub_parts), preset="planSub", color_id="dkMid", node_id=E("T")),
    ], gap=3, width="fill", node_id=E("S"))]
    if badge:
        head.append(fk.stack(
            [fk.text(fk.rich(badge), preset="badge", color_id="ink", align="center",
                     width="hug", node_id=E("T"))],
            width="hug", padding=fk.pad(5, 9, 9, 5), corner=fk.radius(7),
            fill_=fk.fill("mari"), align_h="center", align_v="center", node_id=E("S")))

    return fk.on_selected(
        fk.product([
            fk.stack(head, direction="horizontal", gap=8, align_v="center", width="fill",
                     node_id=E("S")),
            fk.text(fk.rich(fk.Var(price_var)), preset="price", color_id="onInk",
                    node_id=E("T")),
        ], product_id=product_id, group_id="plans", default=default,
            width="fill", gap=5, padding=fk.pad(14, 16, 16, 14), corner=fk.radius(16),
            fill_=fk.fill("dkCard"), border="dkLine", node_id=E("S")),
        fill=fk.fill("dkOn"),
        border={"color": fk.color("mari"), "style": "solid", "width": 1},
        padding=fk.pad(14, 16, 16, 14), borderRadius=fk.radius(16))


PW = {**SCREEN, "fill_": fk.fill("dkBg"), "padding": fk.pad(8, 0, 0, 12), "gap": 14,
      "status_bar_theme": "light"}

scr_paywall = fk.screen(
    "scr_paywall",
    [
        body_pad([
            # Close is an X, not a buried "view other plans" link — both plans are here.
            fk.stack([
                fk.stack([], width="fill", node_id=E("S")),
                fk.stack([fk.icon("X", size_pt=16, color_id="dkMid", weight=IW["X"],
                                  node_id=E("I"))],
                         fixed_w=32, fixed_h=32, corner=fk.radius(16),
                         fill_=fk.fill("dkCard"), align_h="center", align_v="center",
                         actions=[fk.close()], node_id=E("S")),
            ], direction="horizontal", width="fill", align_v="center", node_id=E("S")),

            fk.text(PW_TITLE, preset="h2", color_id="onInk", node_id=E("T")),

            fk.stack([
                bullet("ListChecks", "1,700+ summaries",
                       "Fifteen minutes each, new titles weekly",
                       tint="dkCard", glyph="mari", ink="onInk", ink_sub="dkMid"),
                bullet("Lightning", "Read or listen",
                       "On the commute, the walk, the queue",
                       tint="dkCard", glyph="mari", ink="onInk", ink_sub="dkMid"),
                bullet("Check", "Your plan, kept up to date",
                       "Picks change as your goal does — and streaks keep it alive",
                       tint="dkCard", glyph="mari", ink="onInk", ink_sub="dkMid"),
            ], gap=12, node_id=E("S")),

            # Proof at the decision point. One real, verbatim App Store review — a second
            # card would need a second real quote, and an invented one is a fabricated
            # proof number wearing a person's name.
            fk.stack([
                fk.stack([stars(size_pt=12),
                          fk.text(fk.rich("4.6 · 150K+ ratings"), preset="small",
                                  color_id="dkMid", width="hug", node_id=E("T"))],
                         direction="horizontal", gap=8, align_v="center", node_id=E("S")),
                fk.text(fk.rich("“I never have time to read a full book and often "
                                "feel frustrated by that. These summaries have been "
                                "helpful.”"),
                        preset="small", color_id="onInk", node_id=E("T")),
                fk.text(fk.rich("Susan O'Neill · App Store"), preset="legal",
                        color_id="dkSoft", node_id=E("T")),
            ], gap=6, padding=fk.pad(12, 14, 14, 12), corner=fk.radius(14),
                fill_=fk.fill("dkCard"), node_id=E("S")),

            # Both plans visible. The per-month figure on the annual card is derived by the
            # SDK from the real store price — that is the savings visualization, with no
            # invented percentage.
            fk.stack([
                plan_card(YEAR, "12 months",
                          f"{YEAR}.prod_price",
                          [fk.Var(f"{YEAR}.prod_price_per_month"),
                           " per month, billed yearly"],
                          default=True, badge="BEST VALUE"),
                plan_card(MONTH, "1 month",
                          f"{MONTH}.prod_price",
                          ["Billed monthly, cancel whenever"]),
            ], gap=10, node_id=E("S")),
        ], gap=12, pad=(4, 20, 20, 0)),

        fk.footer([
            fk.stack([fk.text(fk.rich("Start reading"), preset="btn", color_id="ink",
                              align="center", node_id=E("T"))],
                     width="fill", fixed_h=58, corner=fk.radius(16),
                     fill_=fk.fill("mari"), align_h="center", align_v="center",
                     actions=[fk.purchase("plans")], node_id=E("S")),
            fk.text(fk.rich("Cancel anytime in the App Store."), preset="small",
                    color_id="dkMid", align="center", node_id=E("T")),
            fk.stack([
                fk.text(fk.rich("Terms"), preset="legal", color_id="dkSoft", width="hug",
                        align="center",
                        actions=[fk.open_url("https://headway.app/terms", external=True,
                                             action_id="act_terms")], node_id=E("T")),
                fk.text(fk.rich("Privacy"), preset="legal", color_id="dkSoft", width="hug",
                        align="center",
                        actions=[fk.open_url("https://headway.app/privacy", external=True,
                                             action_id="act_privacy")], node_id=E("T")),
                fk.text(fk.rich("Restore"), preset="legal", color_id="dkSoft", width="hug",
                        align="center",
                        actions=[fk.restore()], node_id=E("T")),
            ], direction="horizontal", gap=18, align_h="center", width="fill",
                node_id=E("S")),
        ], fill_=fk.fill("dkBg"), padding=fk.pad(12, 20, 24, 20), gap=10, node_id=E("S")),
    ],
    caption="Paywall — goal-personalized, dark",
    selectable_groups=[{"id": "plans", "type": "product"}],
    progress_bar=False, **PW)


# ============================================================== assemble
cfg = fk.config(
    screens=[scr_hook, scr_method, scr_goal, scr_obstacle, scr_pace, scr_titles,
             scr_building, scr_plan, scr_pact, scr_paywall],
    colors=[(i, n, hx, hx) for i, n, hx in COLORS],  # dark mirrors light: one system
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
