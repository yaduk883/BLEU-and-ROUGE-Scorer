import streamlit as st
import pandas as pd
import requests
from io import StringIO

# ------------------------------------------
# Google Sheet CSV Link
# ------------------------------------------
GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/10foSwd8HyCbltVFYT5HpuiiQMk9FFIkn-aVhH93_A78/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=600)
def load_data():
    try:
        response = requests.get(GOOGLE_SHEET_CSV)
        df = pd.read_csv(StringIO(response.text))
        df.columns = df.columns.str.strip()
        df = df[df['Name of Book'].notna()]
        return df
    except Exception as e:
        st.error(f"⚠️ Failed to load book data: {e}")
        return pd.DataFrame()

# ------------------------------------------
# Page Config
# ------------------------------------------
st.set_page_config(
    page_title="Yadu's Library",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------
# Custom CSS — Dark editorial luxury aesthetic
# ------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@300;400&family=Jost:wght@200;300;400;500&display=swap');

/* ── ROOT & BACKGROUND ── */
:root {
    --cream:    #F5F0E8;
    --ink:      #1A1510;
    --brown:    #5C3D2E;
    --gold:     #C9A84C;
    --sage:     #7A8C74;
    --warm-mid: #2E261D;
    --mid:      #3D3228;
    --border:   rgba(201,168,76,0.25);
    --glass:    rgba(30,22,14,0.6);
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0F0C08 !important;
}

[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(92,61,46,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 90%, rgba(201,168,76,0.08) 0%, transparent 55%);
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1208 0%, #0F0C08 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    font-family: 'Jost', sans-serif !important;
    color: var(--cream) !important;
}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stTextInput input:focus {
    background: rgba(201,168,76,0.07) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--cream) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #C9A84C 0%, #A07832 100%) !important;
    color: #0F0C08 !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 3px !important;
    width: 100% !important;
    padding: 0.55rem 1rem !important;
    margin-top: 0.5rem !important;
    transition: opacity 0.2s !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    opacity: 0.85 !important;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] .sidebar-header {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.1rem !important;
    color: var(--gold) !important;
    letter-spacing: 0.05em !important;
}

/* ── GLOBAL TEXT ── */
* {
    color: var(--cream);
    font-family: 'Jost', sans-serif;
}

h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 300 !important;
    color: var(--cream) !important;
}

/* ── MAIN TITLE BLOCK ── */
.library-hero {
    text-align: center;
    padding: 3rem 2rem 2rem;
    position: relative;
}
.library-hero::before {
    content: '';
    display: block;
    width: 60px;
    height: 1px;
    background: var(--gold);
    margin: 0 auto 1.5rem;
}
.library-hero::after {
    content: '';
    display: block;
    width: 60px;
    height: 1px;
    background: var(--gold);
    margin: 1.5rem auto 0;
}
.library-hero .eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.library-hero h1 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: clamp(2.8rem, 5vw, 4.5rem) !important;
    font-weight: 300 !important;
    line-height: 1.1 !important;
    letter-spacing: -0.01em !important;
    color: var(--cream) !important;
    margin: 0 !important;
}
.library-hero h1 em {
    font-style: italic;
    color: var(--gold);
}
.library-hero .subtitle {
    font-family: 'Jost', sans-serif;
    font-weight: 200;
    font-size: 0.85rem;
    letter-spacing: 0.15em;
    color: rgba(245,240,232,0.45);
    text-transform: uppercase;
    margin-top: 1rem;
}

/* ── STAT CARDS ── */
.stat-row {
    display: flex;
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin: 1.5rem 0 2.5rem;
}
.stat-card {
    flex: 1;
    background: #1A1208;
    padding: 1.25rem 1rem;
    text-align: center;
}
.stat-card .stat-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 300;
    color: var(--gold);
    line-height: 1;
}
.stat-card .stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    color: rgba(245,240,232,0.4);
    text-transform: uppercase;
    margin-top: 0.35rem;
}

/* ── SEARCH BOX ── */
.stTextInput > div > div > input {
    background: rgba(201,168,76,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--cream) !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 300 !important;
    padding: 0.75rem 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.12) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: rgba(245,240,232,0.28) !important;
    font-style: italic !important;
}
.stTextInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    color: var(--gold) !important;
    text-transform: uppercase !important;
    margin-bottom: 0.4rem !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] table {
    background: #12100A !important;
}
[data-testid="stDataFrame"] thead th {
    background: #1A1208 !important;
    color: var(--gold) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stDataFrame"] tbody td {
    background: transparent !important;
    color: var(--cream) !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 300 !important;
    border-bottom: 1px solid rgba(201,168,76,0.08) !important;
    padding: 0.65rem 1rem !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
    background: rgba(201,168,76,0.05) !important;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    color: var(--gold) !important;
    text-transform: uppercase !important;
}
[data-testid="stSelectbox"] > div > div {
    background: rgba(201,168,76,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--cream) !important;
    font-family: 'Jost', sans-serif !important;
}

/* ── DESCRIPTION CARD ── */
.desc-card {
    background: linear-gradient(135deg, #1E1610 0%, #14100A 100%);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: 0 6px 6px 0;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
}
.desc-card .desc-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    font-style: italic;
    color: var(--cream);
    margin-bottom: 0.75rem;
}
.desc-card .desc-body {
    font-family: 'Jost', sans-serif;
    font-weight: 300;
    font-size: 0.92rem;
    color: rgba(245,240,232,0.65);
    line-height: 1.75;
}

/* ── RESULTS BADGE ── */
.results-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(122,140,116,0.15);
    border: 1px solid rgba(122,140,116,0.35);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    color: var(--sage);
    margin-bottom: 1rem;
}
.results-badge .dot {
    width: 6px;
    height: 6px;
    background: var(--sage);
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    border: 1px dashed rgba(201,168,76,0.2);
    border-radius: 8px;
    margin: 1rem 0;
}
.empty-state .icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}
.empty-state p {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    font-style: italic;
    color: rgba(245,240,232,0.35);
}

/* ── DIVIDER ── */
.gold-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2.5rem 0;
}
.gold-divider::before,
.gold-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border));
}
.gold-divider::after {
    background: linear-gradient(90deg, var(--border), transparent);
}
.gold-divider span {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: var(--gold);
    opacity: 0.6;
    text-transform: uppercase;
    white-space: nowrap;
}

/* ── ADMIN FORM ── */
.admin-header {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.6rem !important;
    font-style: italic !important;
    color: var(--gold) !important;
    margin-bottom: 0.25rem !important;
}
.admin-subtext {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: rgba(245,240,232,0.3);
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.stTextInput input, .stNumberInput input, .stTextArea textarea,
.stSelectbox > div > div, .stDateInput input {
    background: rgba(201,168,76,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--cream) !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 300 !important;
}
.stTextArea textarea {
    font-size: 0.9rem !important;
    line-height: 1.7 !important;
}

.stTextArea label,
.stNumberInput label,
.stDateInput label,
.stSelectbox label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.18em !important;
    color: var(--gold) !important;
    text-transform: uppercase !important;
}

/* ── SUBMIT BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #C9A84C 0%, #8C6820 100%) !important;
    color: #0F0C08 !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.65rem 2rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(201,168,76,0.3) !important;
}

/* ── ALERTS ── */
.stSuccess > div {
    background: rgba(122,140,116,0.12) !important;
    border: 1px solid rgba(122,140,116,0.3) !important;
    border-radius: 4px !important;
    color: var(--sage) !important;
    font-family: 'Jost', sans-serif !important;
}
.stWarning > div {
    background: rgba(201,168,76,0.08) !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 4px !important;
    color: var(--gold) !important;
    font-family: 'Jost', sans-serif !important;
}
.stInfo > div {
    background: rgba(92,61,46,0.15) !important;
    border: 1px solid rgba(92,61,46,0.3) !important;
    border-radius: 4px !important;
    color: rgba(245,240,232,0.55) !important;
    font-family: 'Jost', sans-serif !important;
}
.stError > div {
    background: rgba(180,60,50,0.1) !important;
    border: 1px solid rgba(180,60,50,0.3) !important;
    border-radius: 4px !important;
}

/* ── SIDEBAR LABELS ── */
[data-testid="stSidebar"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.18em !important;
    color: var(--gold) !important;
    text-transform: uppercase !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# Load Data
# ------------------------------------------
book_data = load_data()

if 'Sl No' in book_data.columns:
    book_data.drop(columns=['Sl No'], inplace=True)

display_columns = [
    'Name of Book', 'Author', 'Language', 'N.o of Copies',
    'Date', 'BAR CODE', 'Available/Not', 'Checked Out By'
]

# ------------------------------------------
# Sidebar — Admin Login
# ------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 2rem 0 1.5rem;">
        <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.25em;
                    color:rgba(201,168,76,0.5);text-transform:uppercase;margin-bottom:0.5rem;">
            Restricted Access
        </div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;
                    font-style:italic;color:#C9A84C;">
            Admin Portal
        </div>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login = st.button("Authenticate")

    is_admin = False
    if login:
        if username == "admin" and password == "admin123":
            st.success("Access granted")
            is_admin = True
        else:
            st.error("Invalid credentials")

    st.markdown("""
    <div style="position:absolute;bottom:2rem;left:1.5rem;right:1.5rem;
                border-top:1px solid rgba(201,168,76,0.15);padding-top:1rem;">
        <div style="font-family:'DM Mono',monospace;font-size:0.58rem;
                    letter-spacing:0.12em;color:rgba(245,240,232,0.18);text-transform:uppercase;">
            Yadu's Personal Library<br>Est. Collection
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# Hero Section
# ------------------------------------------
st.markdown("""
<div class="library-hero">
    <div class="eyebrow">Personal Collection</div>
    <h1>Yadu's <em>Library</em></h1>
    <div class="subtitle">A curated archive of books & knowledge</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------
# Stats Row
# ------------------------------------------
if not book_data.empty:
    total_books = len(book_data)
    avail_col = 'Available/Not'
    available = book_data[book_data[avail_col].str.lower().str.contains('available', na=False)].shape[0] if avail_col in book_data.columns else "—"
    languages = book_data['Language'].nunique() if 'Language' in book_data.columns else "—"
    authors = book_data['Author'].nunique() if 'Author' in book_data.columns else "—"

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-num">{total_books}</div>
            <div class="stat-label">Total Titles</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{available}</div>
            <div class="stat-label">Available</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{authors}</div>
            <div class="stat-label">Authors</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{languages}</div>
            <div class="stat-label">Languages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# Search
# ------------------------------------------
query = st.text_input(
    "Search the Collection",
    placeholder="Title, author, subject…",
    key="search_input"
)

# ------------------------------------------
# Results
# ------------------------------------------
if query:
    query_lower = query.lower()
    filtered = book_data[
        book_data['Name of Book'].str.lower().str.contains(query_lower, na=False) |
        book_data['Author'].str.lower().str.contains(query_lower, na=False)
    ]
else:
    filtered = pd.DataFrame()

if not filtered.empty:
    st.markdown(f"""
    <div class="results-badge">
        <span class="dot"></span>
        {len(filtered)} result{'s' if len(filtered) != 1 else ''} found for "{query}"
    </div>
    """, unsafe_allow_html=True)

    show_cols = [col for col in display_columns if col in filtered.columns]
    st.dataframe(filtered[show_cols], use_container_width=True, hide_index=True)

    st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
    selected_book = st.selectbox(
        "View Book Description",
        filtered['Name of Book'].dropna().unique(),
        key="book_select"
    )

    if selected_book and 'Description' in filtered.columns:
        desc = filtered.loc[
            filtered['Name of Book'].str.strip() == selected_book.strip(),
            'Description'
        ].values
        desc_text = desc[0] if len(desc) > 0 and pd.notna(desc[0]) else "No description available for this title."
        st.markdown(f"""
        <div class="desc-card">
            <div class="desc-title">{selected_book}</div>
            <div class="desc-body">{desc_text}</div>
        </div>
        """, unsafe_allow_html=True)

elif query:
    st.markdown(f"""
    <div class="empty-state">
        <div class="icon">◎</div>
        <p>No titles found matching "{query}"</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">✦</div>
        <p>Begin typing to search the collection…</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# Admin — Add New Book
# ------------------------------------------
if is_admin:
    st.markdown("""
    <div class="gold-divider"><span>Admin Controls</span></div>
    <div class="admin-header">Add New Title</div>
    <div class="admin-subtext">Append a new entry to the library catalogue</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        new_name = st.text_input("Book Name", key="an")
        new_author = st.text_input("Author", key="aa")
        new_lang = st.text_input("Language", key="al")
        new_date = st.date_input("Acquisition Date", key="ad")

    with col2:
        new_copies = st.number_input("No. of Copies", min_value=1, value=1, key="ac")
        new_barcode = st.text_input("Barcode", key="ab")
        new_avail = st.selectbox("Availability", ["Available", "Not Available"], key="av")
        new_user = st.text_input("Checked Out By", key="au")

    new_desc = st.text_area("Synopsis / Description", height=120, key="adesc")

    st.markdown('<div style="margin-top:1rem;"></div>', unsafe_allow_html=True)
    if st.button("Add to Catalogue"):
        if new_name:
            st.success(f"'{new_name}' has been registered in the catalogue.")
        else:
            st.warning("Please enter a book name before submitting.")
        # NOTE: To actually append to Google Sheet, you'd need gspread + service account setup
