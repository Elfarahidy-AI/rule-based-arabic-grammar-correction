# Arabic Grammar Correction using Rule-Based Algorithms

This project aims to detect and correct grammatical errors in Arabic text using rule-based algorithms. It leverages a Conditional Random Field (CRF) model for Part-of-Speech (POS) tagging to identify the indices of verbs in the text. The correction process relies on the identified verb indices and a predefined set of special words to assist in grammar correction.
Features

- Detects grammatical errors in Arabic text using rule-based algorithms.
- Utilizes a CRF model for accurate POS tagging of each word in the text.
- Identifies the indices of verbs in the text based on the POS tags.
- Employs a predefined set of special words to aid in grammar correction.
- Provides corrected Arabic text with improved grammatical accuracy.

## Installation

#### Clone the repository:

    git clone https://github.com/your-username/arabic-grammar-correction.git

#### Install the required dependencies:


    pip install -r requirements.txt

    Download the pre-trained CRF model for POS tagging and place it in the models directory.

#### Usage

    text = (
    "الاولاد يلعبون الكرة ولكن المعلمون لا يشاهدينهم. "
    "لا ترجون رحمة احد غير الله. "
    "وكان المعلمون متميزون والاولاد مثلهم. "
    "الأولاد ناموا ولن يشاهون التلفاز. "
    "وهذان المعلمين متميزون."
    "اصبح المعلمين متميزين."
    "ان صائدون السمك يبحروا."
    "رجع المعلمين الى المدرسة."
    "الطلاب المتميزين لا يشاهدوا التلفاز."
    )

#### Output:
    الأولاد يلعبون الكرة ولكن المعلمين لا يشاهدونهم . 
    لا ترجوا رحمة أحد غير الله . 
    وكان المعلمون متميزون والأولاد مثلهم . 
    الأولاد ناموا ولن يشاهوا التلفاز . 
    وهذان المعلمان متميزان . 
    أصبح المعلمون متميزين . 
    أن صائدي السمك يبحرون . 
    رجع المعلمون إلى المدرسة . 
    الطلاب المتميزون لا يشاهدون التلفاز .


## Rule-Based Algorithms

The project employs several rule-based algorithms to detect and correct grammatical errors in Arabic text.

The following is a list of grammatical errors that the project currently detects and fixes:

    تصحيح الهمزات كلها
    تصحيح دمج كلمتين
    تصحيح بعض اخطاء الفصل (فصل كلمتين)
    رفع الفعل المضارع
    نصب الفعل المضارع
    جزم الفعل المضارع
    تصحيح و جر الإسم المجرور اذا كان مرفوع بالخطأ
    ضبط المضاف إليه بعد ظرف الزمان او المكان
    ضبط النعت
    ضبط اسماء الإشارة و ما بعدها
    تصحيح المثنى للجمع او الجمع للمثنى في حالة التعامل مع مع اسماء الإشارة
    تصحيح اسم كان واخواتها
    تصحيح اسم ان واخواتها
    ضبط بعض اجزاء الجملة الإسمية
    ضبط العطف و المعطوف
    ضبط التوكيد

Data

The project utilizes the following data sources:

- CRF Model: A pre-trained Conditional Random Field model for Arabic POS tagging. The model is used to assign POS tags to each word in the input text.
- Special Words: A predefined set of special words that aid in grammar correction, such as specific prepositions, conjunctions, and pronouns.
