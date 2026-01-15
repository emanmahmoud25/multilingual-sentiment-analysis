import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_pie_chart_base64(summary: dict):
    labels = list(summary.keys())
    sizes = list(summary.values())

    plt.figure(figsize=(3, 3), dpi=100)
    plt.pie(
        sizes,
        labels=labels,
        autopct="%1.0f%%",
        startangle=90,
        textprops={"fontsize": 9}
    )
    plt.axis("equal")

    buffer = BytesIO()
    plt.savefig(buffer, format="PNG", bbox_inches="tight")
    plt.close()

    return base64.b64encode(buffer.getvalue()).decode()