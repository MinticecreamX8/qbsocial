import tkinter as tk
from tkinter import ttk, scrolledtext
from twitter_client import search_twitter

TOPIC_FILE = "topic.txt"
KEY_FILE = "key.txt"


def load_topic():
    try:
        with open(TOPIC_FILE, "r") as f:
            return f.read().strip()
    except:
        return ""


def load_key():
    try:
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    except:
        return ""


def save_key(key):
    with open(KEY_FILE, "w") as f:
        f.write(key.strip())


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitter OS Viewer")
        self.root.geometry("750x600")

        # -------------------
        # TAB SYSTEM
        # -------------------
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        # TAB 1: FEED
        self.feed_tab = tk.Frame(self.tabs)
        self.tabs.add(self.feed_tab, text="Feed")

        # TAB 2: KEY SETTINGS
        self.key_tab = tk.Frame(self.tabs)
        self.tabs.add(self.key_tab, text="Key")

        # -------------------
        # FEED TAB UI
        # -------------------
        self.output = scrolledtext.ScrolledText(self.feed_tab, width=85, height=30)
        self.output.pack(pady=10)

        tk.Button(self.feed_tab, text="Refresh Feed", command=self.run_search).pack()

        # -------------------
        # KEY TAB UI
        # -------------------
        tk.Label(self.key_tab, text="API Key (Bearer Token)").pack(pady=10)

        self.key_entry = tk.Entry(self.key_tab, width=60)
        self.key_entry.pack()

        tk.Button(self.key_tab, text="Load Existing Key", command=self.load_key_to_box).pack(pady=5)
        tk.Button(self.key_tab, text="Save Key", command=self.save_key_from_box).pack(pady=5)

        # auto-load feed
        self.run_search()

    # -------------------
    # FEED LOGIC
    # -------------------
    def run_search(self):
        topic = load_topic()

        self.output.delete("1.0", tk.END)

        if not topic:
            self.output.insert(tk.END, "No topic found in topic.txt\n")
            return

        results = search_twitter(topic)

        self.output.insert(tk.END, f"TOPIC: {topic}\n\n")

        for r in results:
            self.output.insert(tk.END, f"- {r}\n\n")

    # -------------------
    # KEY LOGIC
    # -------------------
    def load_key_to_box(self):
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, load_key())

    def save_key_from_box(self):
        key = self.key_entry.get().strip()
        save_key(key)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()