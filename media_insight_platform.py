"""传媒资讯交互数据分析平台.

期末作品：Tkinter + Matplotlib + Turtle 综合创作。
运行方式：python media_insight_platform.py
"""

from __future__ import annotations

import csv
import math
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Iterable

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


ALL = "全部"
CHART_BAR = "热度柱状图"
CHART_DONUT = "题材圆环图"
CHART_TREND = "周浏览趋势"
CHART_CHANNEL = "渠道对比图"


@dataclass(frozen=True)
class MediaItem:
    title: str
    category: str
    channel: str
    views: int
    likes: int
    comments: int
    shares: int
    duration_min: int
    day: str


MEDIA_DATA: list[MediaItem] = [
    MediaItem("城市烟火气短视频", "民生", "短视频号", 156000, 10400, 1860, 2710, 3, "周一"),
    MediaItem("亚运场馆焕新报道", "体育", "新闻客户端", 98000, 7100, 930, 1210, 5, "周一"),
    MediaItem("AI主播一分钟快讯", "科技", "融媒直播间", 213000, 15800, 2410, 3920, 2, "周二"),
    MediaItem("非遗手艺人专题", "文化", "电视栏目", 78000, 6100, 700, 980, 12, "周二"),
    MediaItem("校园毕业季采访", "教育", "短视频号", 132000, 8600, 1450, 2100, 4, "周三"),
    MediaItem("夜间经济观察", "财经", "新闻客户端", 118000, 7900, 1080, 1550, 6, "周三"),
    MediaItem("博物馆奇妙夜直播", "文化", "融媒直播间", 240000, 18300, 3200, 4600, 45, "周四"),
    MediaItem("雨天通勤服务信息", "民生", "新闻客户端", 87000, 5200, 640, 820, 3, "周四"),
    MediaItem("国产游戏出海观察", "科技", "电视栏目", 165000, 11100, 1720, 2490, 15, "周五"),
    MediaItem("乡村篮球赛现场", "体育", "短视频号", 188000, 13900, 2150, 3310, 7, "周五"),
    MediaItem("暑期研学消费指南", "教育", "新闻客户端", 93000, 6500, 860, 1170, 6, "周六"),
    MediaItem("年轻人理财微调查", "财经", "短视频号", 126000, 8300, 1190, 1760, 5, "周六"),
    MediaItem("城市更新深度访谈", "民生", "电视栏目", 102000, 6900, 950, 1320, 18, "周日"),
    MediaItem("周末文旅榜单", "文化", "新闻客户端", 174000, 12200, 1870, 2880, 4, "周日"),
    MediaItem("高温天气服务直播", "民生", "融媒直播间", 198000, 14200, 2760, 4180, 35, "周一"),
    MediaItem("青年夜校选课指南", "教育", "新闻客户端", 112000, 7600, 1080, 1510, 4, "周二"),
    MediaItem("城市音乐节幕后花絮", "文化", "短视频号", 221000, 17100, 2890, 4430, 6, "周三"),
    MediaItem("社区养老服务观察", "民生", "电视栏目", 91000, 5900, 820, 1050, 16, "周四"),
    MediaItem("低空经济科普短片", "科技", "短视频号", 176000, 12700, 1940, 3020, 5, "周五"),
    MediaItem("高校运动会开幕式", "体育", "融媒直播间", 205000, 14900, 2260, 3510, 28, "周六"),
    MediaItem("县域文旅新玩法", "文化", "电视栏目", 139000, 9600, 1360, 1880, 14, "周日"),
    MediaItem("新能源车消费问答", "财经", "新闻客户端", 151000, 10300, 1640, 2260, 7, "周一"),
    MediaItem("智能眼镜体验测评", "科技", "短视频号", 234000, 19200, 3460, 5120, 8, "周二"),
    MediaItem("校园心理健康访谈", "教育", "电视栏目", 84000, 5400, 750, 980, 20, "周三"),
    MediaItem("地铁新线试乘报道", "民生", "新闻客户端", 169000, 11100, 1730, 2480, 5, "周四"),
    MediaItem("女足城市邀请赛", "体育", "短视频号", 147000, 9800, 1410, 2210, 4, "周五"),
    MediaItem("国潮品牌直播间", "财经", "融媒直播间", 219000, 16200, 2550, 3980, 42, "周六"),
    MediaItem("纪录片片花首发", "文化", "短视频号", 187000, 13900, 2100, 3340, 3, "周日"),
]

SAMPLE_CASES = [
    ("文化内容复盘", "题材=文化，渠道=全部", "观察文旅、非遗、纪录片等内容的平均热度，适合新闻选题复盘。"),
    ("短视频表现评估", "题材=全部，渠道=短视频号", "比较短视频标题、时长和互动数据，判断哪些内容适合二次剪辑。"),
    ("直播栏目答辩展示", "题材=全部，渠道=融媒直播间", "突出直播内容的浏览量和转发率，适合展示综合创作能力。"),
    ("民生服务信息分析", "题材=民生，关键词=服务", "验证关键词搜索能力，并说明服务类资讯的实际业务价值。"),
]


def heat_score(item: MediaItem) -> float:
    """计算综合传播热度，兼顾浏览、互动和内容时长。"""
    interaction = item.likes * 0.45 + item.comments * 1.8 + item.shares * 2.2
    duration_bonus = min(item.duration_min, 20) * 120
    return round(item.views * 0.08 + interaction + duration_bonus, 2)


def heat_level(score: float) -> str:
    if score >= 36000:
        return "爆款"
    if score >= 24000:
        return "高热"
    if score >= 15000:
        return "稳健"
    return "培育"


def format_number(value: int | float) -> str:
    return f"{value:,.0f}"


def categories() -> list[str]:
    return [ALL] + sorted({item.category for item in MEDIA_DATA})


def channels() -> list[str]:
    return [ALL] + sorted({item.channel for item in MEDIA_DATA})


def filter_items(category: str, channel: str, keyword: str) -> list[MediaItem]:
    keyword = keyword.strip().lower()
    filtered: list[MediaItem] = []
    for item in MEDIA_DATA:
        category_ok = category == ALL or item.category == category
        channel_ok = channel == ALL or item.channel == channel
        keyword_ok = not keyword or keyword in item.title.lower()
        if category_ok and channel_ok and keyword_ok:
            filtered.append(item)
    return filtered


def summarize(items: Iterable[MediaItem]) -> dict[str, float]:
    rows = list(items)
    if not rows:
        return {"count": 0, "views": 0, "likes": 0, "avg_heat": 0, "share_rate": 0, "comments": 0}
    total_views = sum(item.views for item in rows)
    total_likes = sum(item.likes for item in rows)
    total_comments = sum(item.comments for item in rows)
    total_shares = sum(item.shares for item in rows)
    avg_heat = sum(heat_score(item) for item in rows) / len(rows)
    share_rate = total_shares / total_views * 100
    return {
        "count": len(rows),
        "views": total_views,
        "likes": total_likes,
        "comments": total_comments,
        "avg_heat": avg_heat,
        "share_rate": share_rate,
    }


def category_heat(items: Iterable[MediaItem]) -> dict[str, float]:
    totals: dict[str, list[float]] = {}
    for item in items:
        totals.setdefault(item.category, []).append(heat_score(item))
    return {name: sum(scores) / len(scores) for name, scores in totals.items()}


def day_views(items: Iterable[MediaItem]) -> dict[str, int]:
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    totals = {day: 0 for day in days}
    for item in items:
        totals[item.day] += item.views
    return totals


def channel_views(items: Iterable[MediaItem]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for item in items:
        totals[item.channel] = totals.get(item.channel, 0) + item.views
    return totals


class MediaInsightApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("传媒资讯交互数据分析平台")
        self.geometry("1260x800")
        self.minsize(1050, 690)

        self.current_items: list[MediaItem] = list(MEDIA_DATA)
        self.chart_canvas: FigureCanvasTkAgg | None = None

        self._configure_style()
        self._build_menu()
        self._build_layout()
        self.refresh_data()

    def _configure_style(self) -> None:
        self.colors = {
            "bg": "#eef3f8",
            "panel": "#ffffff",
            "ink": "#14233a",
            "muted": "#66758a",
            "line": "#d8e2ef",
            "blue": "#1f6fb2",
            "green": "#1b9a76",
            "gold": "#d99a18",
            "red": "#d85d55",
        }
        self.configure(bg=self.colors["bg"])
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Panel.TFrame", background=self.colors["panel"], relief="flat")
        style.configure("Card.TFrame", background=self.colors["panel"], relief="flat")
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["ink"], font=("Microsoft YaHei UI", 10))
        style.configure("Panel.TLabel", background=self.colors["panel"], foreground=self.colors["ink"], font=("Microsoft YaHei UI", 10))
        style.configure("Muted.TLabel", background=self.colors["panel"], foreground=self.colors["muted"], font=("Microsoft YaHei UI", 9))
        style.configure("Title.TLabel", background=self.colors["bg"], foreground=self.colors["ink"], font=("Microsoft YaHei UI", 20, "bold"))
        style.configure("Subtitle.TLabel", background=self.colors["bg"], foreground=self.colors["muted"], font=("Microsoft YaHei UI", 10))
        style.configure("Section.TLabel", background=self.colors["panel"], foreground=self.colors["ink"], font=("Microsoft YaHei UI", 12, "bold"))
        style.configure("Metric.TLabel", background=self.colors["panel"], foreground=self.colors["blue"], font=("Microsoft YaHei UI", 15, "bold"))
        style.configure("TButton", font=("Microsoft YaHei UI", 10), padding=(12, 8), borderwidth=0)
        style.configure("Accent.TButton", background=self.colors["blue"], foreground="#ffffff")
        style.configure("Soft.TButton", background="#e9f1fb", foreground=self.colors["blue"])
        style.map("Accent.TButton", background=[("active", "#16598e")])
        style.map("Soft.TButton", background=[("active", "#dbeaf8")])
        style.configure("TRadiobutton", background=self.colors["panel"], font=("Microsoft YaHei UI", 10))
        style.configure("TCombobox", padding=(8, 5))
        style.configure("Treeview", background="#fbfdff", fieldbackground="#fbfdff", foreground=self.colors["ink"], font=("Microsoft YaHei UI", 10), rowheight=32, borderwidth=0)
        style.configure("Treeview.Heading", background="#e7eef7", foreground=self.colors["ink"], font=("Microsoft YaHei UI", 10, "bold"), padding=(8, 8))
        style.map("Treeview", background=[("selected", "#cfe4f7")])
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", font=("Microsoft YaHei UI", 10), padding=(16, 9))

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="导出当前数据 CSV", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.destroy)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="作品说明", command=self.show_about)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        menu_bar.add_cascade(label="帮助", menu=help_menu)
        self.config(menu=menu_bar)

    def _build_layout(self) -> None:
        header = ttk.Frame(self, padding=(22, 18, 22, 10))
        header.pack(fill=tk.X)
        title_box = ttk.Frame(header)
        title_box.pack(side=tk.LEFT)
        ttk.Label(title_box, text="传媒资讯交互数据分析平台", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(title_box, text="面向新闻 / 广电专业的选题复盘、传播热度与视觉创作小工具", style="Subtitle.TLabel").pack(anchor=tk.W, pady=(4, 0))
        ttk.Label(header, text=f"示例数据 {len(MEDIA_DATA)} 条", foreground=self.colors["blue"], background=self.colors["bg"], font=("Microsoft YaHei UI", 11, "bold")).pack(side=tk.RIGHT)

        body = ttk.Frame(self, padding=(22, 8, 22, 12))
        body.pack(fill=tk.BOTH, expand=True)

        controls = ttk.Frame(body, style="Panel.TFrame", padding=16)
        controls.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 14))

        ttk.Label(controls, text="筛选与操作", style="Section.TLabel").pack(anchor=tk.W, pady=(0, 4))
        ttk.Label(controls, text="选择一个场景，快速生成分析视图", style="Muted.TLabel").pack(anchor=tk.W, pady=(0, 12))

        self.category_var = tk.StringVar(value=ALL)
        self.channel_var = tk.StringVar(value=ALL)
        self.keyword_var = tk.StringVar()
        self.chart_type_var = tk.StringVar(value=CHART_BAR)

        self._combo(controls, "题材分类", self.category_var, categories())
        self._combo(controls, "发布渠道", self.channel_var, channels())
        self._entry(controls, "标题关键词", self.keyword_var)

        ttk.Button(controls, text="查询数据", style="Accent.TButton", command=self.refresh_data).pack(fill=tk.X, pady=(14, 6))
        ttk.Button(controls, text="重置条件", style="Soft.TButton", command=self.reset_filters).pack(fill=tk.X, pady=6)

        self._separator(controls)
        ttk.Label(controls, text="图表类型", style="Section.TLabel").pack(anchor=tk.W, pady=(0, 8))
        for text in [CHART_BAR, CHART_DONUT, CHART_TREND, CHART_CHANNEL]:
            ttk.Radiobutton(controls, text=text, variable=self.chart_type_var, value=text, command=self.draw_chart).pack(anchor=tk.W, pady=4)
        ttk.Button(controls, text="生成分析图表", style="Soft.TButton", command=self.draw_chart).pack(fill=tk.X, pady=(12, 6))

        self._separator(controls)
        ttk.Label(controls, text="答辩展示", style="Section.TLabel").pack(anchor=tk.W, pady=(0, 8))
        ttk.Button(controls, text="绘制传媒主题标识", command=self.draw_turtle_logo).pack(fill=tk.X, pady=6)
        ttk.Button(controls, text="查看结论建议", command=self.show_recommendation).pack(fill=tk.X, pady=6)

        right = ttk.Frame(body)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_metrics(right)
        self._build_tabs(right)

        self.status_var = tk.StringVar(value="已加载示例数据，等待查询。")
        status = ttk.Frame(self, padding=(22, 0, 22, 12))
        status.pack(fill=tk.X)
        ttk.Label(status, textvariable=self.status_var, foreground=self.colors["muted"], background=self.colors["bg"]).pack(anchor=tk.W)

    def _build_metrics(self, parent: ttk.Frame) -> None:
        self.metrics_frame = ttk.Frame(parent)
        self.metrics_frame.pack(fill=tk.X)
        self.metric_vars = {
            "作品数": tk.StringVar(),
            "总浏览量": tk.StringVar(),
            "总点赞": tk.StringVar(),
            "总评论": tk.StringVar(),
            "平均热度": tk.StringVar(),
            "转发率": tk.StringVar(),
        }
        accent_colors = [self.colors["blue"], self.colors["green"], self.colors["gold"], self.colors["red"], "#6f63bf", "#607080"]
        for index, (label, var) in enumerate(self.metric_vars.items()):
            block = ttk.Frame(self.metrics_frame, style="Card.TFrame", padding=(12, 10))
            block.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0 if index == 0 else 8, 0))
            tk.Frame(block, height=3, bg=accent_colors[index]).pack(fill=tk.X, pady=(0, 8))
            ttk.Label(block, text=label, style="Muted.TLabel").pack(anchor=tk.W)
            ttk.Label(block, textvariable=var, style="Metric.TLabel").pack(anchor=tk.W, pady=(3, 0))

    def _build_tabs(self, parent: ttk.Frame) -> None:
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(14, 0))

        table_tab = ttk.Frame(notebook, padding=10)
        chart_tab = ttk.Frame(notebook, padding=10)
        samples_tab = ttk.Frame(notebook, padding=10)
        explain_tab = ttk.Frame(notebook, padding=10)
        notebook.add(table_tab, text="数据总览")
        notebook.add(chart_tab, text="图表分析")
        notebook.add(samples_tab, text="示例场景")
        notebook.add(explain_tab, text="作品说明")

        columns = ("title", "category", "channel", "views", "likes", "comments", "shares", "heat", "level")
        self.tree = ttk.Treeview(table_tab, columns=columns, show="headings")
        headings = {
            "title": "资讯标题",
            "category": "题材",
            "channel": "渠道",
            "views": "浏览量",
            "likes": "点赞",
            "comments": "评论",
            "shares": "转发",
            "heat": "热度分",
            "level": "等级",
        }
        widths = {"title": 210, "category": 70, "channel": 96, "views": 88, "likes": 76, "comments": 76, "shares": 76, "heat": 86, "level": 66}
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor=tk.CENTER)
        self.tree.column("title", anchor=tk.W)
        self.tree.tag_configure("odd", background="#ffffff")
        self.tree.tag_configure("even", background="#f4f8fc")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(table_tab, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.chart_area = ttk.Frame(chart_tab, style="Panel.TFrame")
        self.chart_area.pack(fill=tk.BOTH, expand=True)

        self.samples = tk.Listbox(samples_tab, font=("Microsoft YaHei UI", 10), activestyle="none", height=7, bg="#fbfdff", bd=0, highlightthickness=1, highlightbackground="#d8e2ef", selectbackground="#cfe4f7")
        self.samples.pack(fill=tk.X, pady=(0, 10))
        for name, condition, detail in SAMPLE_CASES:
            self.samples.insert(tk.END, f"{name}  |  {condition}  |  {detail}")
        self.samples.bind("<<ListboxSelect>>", self.apply_sample_case)

        self.sample_detail = tk.Text(samples_tab, wrap=tk.WORD, font=("Microsoft YaHei UI", 10), padx=14, pady=12, height=9, bg="#fbfdff", relief=tk.FLAT)
        self.sample_detail.pack(fill=tk.BOTH, expand=True)
        self.sample_detail.insert(
            tk.END,
            "点击上方示例场景，可自动填充筛选条件。答辩时可以依次演示：\n\n"
            "1. 选择不同题材，观察热度柱状图变化。\n"
            "2. 切换到周浏览趋势，说明循环统计的结果。\n"
            "3. 点击查看结论建议，展示选择结构和业务解释。\n"
            "4. 点击 Turtle 绘图按钮，展示创意视觉绘制功能。",
        )
        self.sample_detail.configure(state=tk.DISABLED)

        self.explain = tk.Text(explain_tab, wrap=tk.WORD, font=("Microsoft YaHei UI", 10), padx=14, pady=12, height=10, bg="#fbfdff", relief=tk.FLAT)
        self.explain.pack(fill=tk.BOTH, expand=True)
        self.explain.insert(
            tk.END,
            "本作品围绕传媒资讯业务数据展开，使用列表和数据类组织模拟数据，"
            "通过自定义函数完成筛选、统计、热度计算和图表绘制。界面支持题材、渠道、关键词查询，"
            "并提供柱状图、圆环图、趋势图和渠道对比图。Turtle 模块用于绘制融媒体主题标识，"
            "体现数据分析与视觉创作的综合应用。",
        )
        self.explain.configure(state=tk.DISABLED)

    def _combo(self, parent: ttk.Frame, label: str, variable: tk.StringVar, values: list[str]) -> None:
        ttk.Label(parent, text=label, style="Panel.TLabel").pack(anchor=tk.W, pady=(10, 4))
        ttk.Combobox(parent, textvariable=variable, values=values, state="readonly", width=20).pack(fill=tk.X)

    def _entry(self, parent: ttk.Frame, label: str, variable: tk.StringVar) -> None:
        ttk.Label(parent, text=label, style="Panel.TLabel").pack(anchor=tk.W, pady=(10, 4))
        ttk.Entry(parent, textvariable=variable).pack(fill=tk.X, ipady=3)

    def _separator(self, parent: ttk.Frame) -> None:
        ttk.Separator(parent).pack(fill=tk.X, pady=16)

    def apply_sample_case(self, _event=None) -> None:
        selection = self.samples.curselection()
        if not selection:
            return
        index = selection[0]
        name, _condition, detail = SAMPLE_CASES[index]
        if index == 0:
            self.category_var.set("文化")
            self.channel_var.set(ALL)
            self.keyword_var.set("")
            self.chart_type_var.set(CHART_DONUT)
        elif index == 1:
            self.category_var.set(ALL)
            self.channel_var.set("短视频号")
            self.keyword_var.set("")
            self.chart_type_var.set(CHART_BAR)
        elif index == 2:
            self.category_var.set(ALL)
            self.channel_var.set("融媒直播间")
            self.keyword_var.set("")
            self.chart_type_var.set(CHART_CHANNEL)
        elif index == 3:
            self.category_var.set("民生")
            self.channel_var.set(ALL)
            self.keyword_var.set("服务")
            self.chart_type_var.set(CHART_TREND)
        self.refresh_data()
        self.status_var.set(f"已应用示例：{name}。{detail}")

    def reset_filters(self) -> None:
        self.category_var.set(ALL)
        self.channel_var.set(ALL)
        self.keyword_var.set("")
        self.chart_type_var.set(CHART_BAR)
        self.refresh_data()

    def refresh_data(self) -> None:
        self.current_items = filter_items(self.category_var.get(), self.channel_var.get(), self.keyword_var.get())
        self.tree.delete(*self.tree.get_children())
        for index, item in enumerate(self.current_items):
            score = heat_score(item)
            self.tree.insert(
                "",
                tk.END,
                values=(
                    item.title,
                    item.category,
                    item.channel,
                    format_number(item.views),
                    format_number(item.likes),
                    format_number(item.comments),
                    format_number(item.shares),
                    format_number(score),
                    heat_level(score),
                ),
                tags=("even" if index % 2 else "odd",),
            )
        self.update_metrics()
        self.draw_chart()
        self.status_var.set(f"当前显示 {len(self.current_items)} 条资讯记录。")

    def update_metrics(self) -> None:
        summary = summarize(self.current_items)
        self.metric_vars["作品数"].set(f"{summary['count']:.0f}")
        self.metric_vars["总浏览量"].set(format_number(summary["views"]))
        self.metric_vars["总点赞"].set(format_number(summary["likes"]))
        self.metric_vars["总评论"].set(format_number(summary["comments"]))
        self.metric_vars["平均热度"].set(format_number(summary["avg_heat"]))
        self.metric_vars["转发率"].set(f"{summary['share_rate']:.2f}%")

    def draw_chart(self) -> None:
        for child in self.chart_area.winfo_children():
            child.destroy()

        figure = Figure(figsize=(8.8, 5.1), dpi=100, facecolor="#ffffff")
        axis = figure.add_subplot(111)
        chart_type = self.chart_type_var.get()

        if not self.current_items:
            axis.text(0.5, 0.5, "暂无符合条件的数据", ha="center", va="center", fontsize=14)
            axis.set_axis_off()
        elif chart_type == CHART_DONUT:
            self._draw_donut(axis)
        elif chart_type == CHART_TREND:
            self._draw_trend(axis)
        elif chart_type == CHART_CHANNEL:
            self._draw_channel(axis)
        else:
            self._draw_bar(axis)

        figure.tight_layout()
        self.chart_canvas = FigureCanvasTkAgg(figure, master=self.chart_area)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    def _draw_bar(self, axis) -> None:
        sorted_items = sorted(self.current_items, key=heat_score, reverse=True)[:10]
        labels = [item.title[:8] + ("…" if len(item.title) > 8 else "") for item in sorted_items]
        scores = [heat_score(item) for item in sorted_items]
        colors = ["#1f6fb2" if heat_level(score) == "爆款" else "#2f90c8" for score in scores]
        bars = axis.bar(labels, scores, color=colors, width=0.58)
        axis.set_title("资讯作品综合热度 TOP10", fontproperties="Microsoft YaHei", fontsize=14, pad=14)
        axis.set_ylabel("热度分", fontproperties="Microsoft YaHei")
        axis.tick_params(axis="x", rotation=25)
        axis.grid(axis="y", linestyle="--", alpha=0.25)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        for bar, score in zip(bars, scores):
            axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), format_number(score), ha="center", va="bottom", fontsize=8)

    def _draw_donut(self, axis) -> None:
        totals = category_heat(self.current_items)
        labels = list(totals.keys())
        values = list(totals.values())
        colors = ["#1f6fb2", "#1b9a76", "#d99a18", "#d85d55", "#6f63bf", "#607080"]
        wedges, _ = axis.pie(values, startangle=90, colors=colors[: len(values)], wedgeprops={"width": 0.42, "edgecolor": "white"})
        axis.set_title("不同题材平均传播热度占比", fontproperties="Microsoft YaHei", fontsize=14, pad=14)
        axis.legend(wedges, labels, loc="center left", bbox_to_anchor=(0.92, 0.5), frameon=False)
        axis.text(0, 0, "题材\n热度", ha="center", va="center", fontsize=13, fontproperties="Microsoft YaHei", color="#17406d")

    def _draw_trend(self, axis) -> None:
        totals = day_views(self.current_items)
        days = list(totals.keys())
        values = [totals[day] for day in days]
        axis.plot(days, values, marker="o", linewidth=2.6, color="#1b9a76")
        axis.fill_between(days, values, color="#1b9a76", alpha=0.15)
        axis.set_title("一周资讯浏览量趋势", fontproperties="Microsoft YaHei", fontsize=14, pad=14)
        axis.set_ylabel("浏览量", fontproperties="Microsoft YaHei")
        axis.grid(axis="y", linestyle="--", alpha=0.25)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        for x_value, y_value in zip(days, values):
            axis.text(x_value, y_value, format_number(y_value), ha="center", va="bottom", fontsize=8)

    def _draw_channel(self, axis) -> None:
        totals = channel_views(self.current_items)
        labels = list(totals.keys())
        values = list(totals.values())
        bars = axis.barh(labels, values, color=["#1f6fb2", "#1b9a76", "#d99a18", "#d85d55"][: len(labels)])
        axis.set_title("不同发布渠道浏览量对比", fontproperties="Microsoft YaHei", fontsize=14, pad=14)
        axis.set_xlabel("浏览量", fontproperties="Microsoft YaHei")
        axis.grid(axis="x", linestyle="--", alpha=0.25)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        for bar, value in zip(bars, values):
            axis.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f" {format_number(value)}", va="center", fontsize=9)

    def draw_turtle_logo(self) -> None:
        try:
            import turtle

            screen = turtle.Screen()
            screen.title("Turtle 融媒体主题标识")
            screen.bgcolor("#eef3f8")
            pen = turtle.Turtle()
            pen.speed(0)
            pen.hideturtle()
            pen.pensize(3)

            colors = ["#1f6fb2", "#1b9a76", "#d99a18", "#d85d55"]
            for index, color in enumerate(colors):
                pen.penup()
                pen.goto(0, -110 + index * 18)
                pen.pendown()
                pen.color(color)
                pen.circle(110 - index * 15)

            for angle in range(0, 360, 45):
                radians = math.radians(angle)
                pen.penup()
                pen.goto(0, 0)
                pen.pendown()
                pen.color("#17406d")
                pen.goto(math.cos(radians) * 145, math.sin(radians) * 145)
                pen.dot(12, "#d85d55")

            pen.penup()
            pen.goto(-58, -22)
            pen.color("#17406d")
            pen.write("MEDIA", font=("Arial", 22, "bold"))
            pen.goto(-74, -54)
            pen.write("INSIGHT", font=("Arial", 18, "normal"))
        except Exception as exc:  # pragma: no cover - GUI/turtle environment dependent
            messagebox.showerror("绘图失败", f"Turtle 绘图窗口无法打开：{exc}")

    def export_csv(self) -> None:
        path = filedialog.asksaveasfilename(title="导出当前数据", defaultextension=".csv", filetypes=[("CSV 文件", "*.csv")])
        if not path:
            return
        with Path(path).open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["标题", "题材", "渠道", "浏览量", "点赞", "评论", "转发", "时长", "日期", "热度分", "等级"])
            for item in self.current_items:
                score = heat_score(item)
                writer.writerow([item.title, item.category, item.channel, item.views, item.likes, item.comments, item.shares, item.duration_min, item.day, score, heat_level(score)])
        messagebox.showinfo("导出成功", f"已导出 {len(self.current_items)} 条数据。")

    def show_recommendation(self) -> None:
        if not self.current_items:
            messagebox.showinfo("分析结论", "当前没有符合条件的数据，请调整筛选条件。")
            return
        best = max(self.current_items, key=heat_score)
        summary = summarize(self.current_items)
        messagebox.showinfo(
            "分析结论",
            f"当前筛选范围内，热度最高的是《{best.title}》，等级为{heat_level(heat_score(best))}。\n"
            f"平均热度为 {format_number(summary['avg_heat'])}，转发率为 {summary['share_rate']:.2f}%。\n"
            "建议：优先复盘高热题材的标题表达、发布时间和互动引导方式，并将其转化为后续选题策划依据。",
        )

    def show_about(self) -> None:
        messagebox.showinfo("作品说明", "本程序使用 Tkinter 搭建主界面，Matplotlib 完成数据可视化，Turtle 完成传媒主题创意绘图。")


if __name__ == "__main__":
    app = MediaInsightApp()
    app.mainloop()
