from wordcloud import WordCloud
from io import BytesIO
import base64
import arabic_reshaper
from bidi.algorithm import get_display
import pandas as pd
import re
from ..helper.config import settings

AR_STOPWORDS = {
    # حروف جر
    "في", "من", "على", "إلى", "الى", "عن", "مع", "بين", "حول", "ضمن", "خلال", "عبر",

    # ضمائر
    "هو", "هي", "أنا", "انا", "أنت", "انت", "هذا", "هذه", "ذلك",

    # أفعال مساعدة ونفي
    "كان", "كانت", "لم", "ما", "مش", "غير", "بدون",

    # أدوات ربط
    "لكن", "أو", "بل", "إلا","لكنه","لا","كما","ولا","ولن","ليس","أثناء"

    # ظروف
    "هنا", "هناك", "حيث", "عندما", "حين", "حينما", "منذ", "بعد", "قبل", "حتى",

    # استفهام
    "كيف", "متى", "أين", "لماذا", "أي",

    # كلمات عامة
    "جدا", "عموما", "كل", "بعض", "أيضا", "أكثر", "أقل", "كلما", "جدًا","شيء","نوعًا","عام"
}


def is_arabic(word):
    return bool(re.search(r"[\u0600-\u06FF]", word))

def reshape_arabic_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def generate_wordcloud_base64(texts):
    if isinstance(texts, pd.Series):
        texts = texts.dropna().astype(str).tolist()

    if not texts:
        return None

    arabic_words = []
    english_words = []

    for text in texts:
        text = str(text)
        text = re.sub(r"[^\u0600-\u06FFa-zA-Z\s]", " ", text)

        for w in text.split():
            if len(w) < 2:
                continue

            if is_arabic(w):
                if w in AR_STOPWORDS:
                    continue
                arabic_words.append(w)
            else:
                english_words.append(w.lower())

    if not arabic_words and not english_words:
        return None

    final_words = []

    if arabic_words:
        arabic_text = " ".join(arabic_words)
        final_words.append(reshape_arabic_text(arabic_text))

    if english_words:
        final_words.append(" ".join(english_words))

    final_text = " ".join(final_words)

    wc = WordCloud(
        width=500,
        height=350,
        background_color="white",
        font_path=settings.WORDCLOUD_FONT_PATH,
        collocations=False,
        max_words=120
    ).generate(final_text)

    buffer = BytesIO()
    wc.to_image().save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
