// web/tutorial.js - Interactive Dhivehi Coding Academy Curriculum & Validator

const LESSONS = [
  {
    id: 1,
    title: "1. މަރުޙަބާ ދިވެހި ކޯޑު",
    subtitle: "ފުރަތަމަ ޕްރޮގްރާމާއި ލިޔުން ދެއްކުން",
    theory: `
      <h3>ދިވެހި ކޯޑަށް މަރުޙަބާ! 🇲🇻</h3>
      <p>ދިވެހި ކޯޑަކީ ތާނަ އަކުރުން ކޯޑު ލިޔުމަށް ޚާއްޞަކޮށްގެން އުފައްދާފައިވާ ޕްރޮގްރާމިންގ ލެންގުއޭޖެކެވެ.</p>
      <p>ސްކްރީނަށް ނުވަތަ ޓާމިނަލަށް އެއްޗެއް ދެއްކުމަށް ބޭނުންކުރަނީ <code>ދައްކާ</code> ކީވޯޑެވެ.</p>
      <pre><code>ދައްކާ "އައްސަލާމް ޢަލައިކުމް!"</code></pre>
    `,
    task: `<strong>މަސައްކަތް:</strong> <code>ދައްކާ</code> ބޭނުންކޮށްގެން <code>"މަރުޙަބާ ދިވެހިރާއްޖެ"</code> ޓާމިނަލަށް ނެރުއްވާ.`,
    initialCode: `// މިތަނުގައި ތިރީގައިވާ ލިޔުން ލިޔުއްވާ:
// ދައްކާ "މަރުޙަބާ ދިވެހިރާއްޖެ"

ދައްކާ "މަރުޙަބާ ދިވެހިރާއްޖެ"
`,
    expectedMatch: /މަރުޙަބާ ދިވެހިރާއްޖެ/,
    hint: `ދައްކާ "މަރުޙަބާ ދިވެހިރާއްޖެ" ލިޔުއްވާށެވެ.`
  },
  {
    id: 2,
    title: "2. ވެރިއަބަލާއި ހިސާބު",
    subtitle: "ޑޭޓާ ރައްކާކުރުމާއި ހިސާބު ހެދުން",
    theory: `
      <h3>ވެރިއަބަލް (Variables)</h3>
      <p>ޑޭޓާއެއް ނުވަތަ އަގެއް ވަކި ނަމެއްގައި ރައްކާކުރުމަށް <code>ކަނޑައަޅާ</code> ބޭނުންކުރެވެއެވެ.</p>
      <pre><code>ކަނޑައަޅާ ނަން = "ޢަލީ"
ކަނޑައަޅާ އުމުރު = 20</code></pre>
      <p>ހިސާބުގެ އޮޕަރޭޓަރުތައް: <code>+</code>, <code>-</code>, <code>*</code>, <code>/</code></p>
    `,
    task: `<strong>މަސައްކަތް:</strong> <code>ކަނޑައަޅާ އަގު = 50</code> ހެއްދެވުމަށްފަހު، އެ އަގު 2 އިން ގުނަކޮށް (<code>އަގު * 2</code>) ދައްކަވާ (ނަތީޖާއަކަށް 100 ނިކުންނަންވާނެ).`,
    initialCode: `ކަނޑައަޅާ އަގު = 50
// މިތަނުގައި އަގު * 2 ދައްކަވާ:
ދައްކާ އަގު * 2
`,
    expectedMatch: /100/,
    hint: `ދައްކާ އަގު * 2 ލިޔުއްވާށެވެ.`
  },
  {
    id: 3,
    title: "3. ޝަރުޠުތައް (Conditionals)",
    subtitle: "ނަމަ އަދި ނޫންނަމަ ބޭނުންކުރުން",
    theory: `
      <h3>ޝަރުޠީ ބަޔާން (If / Else)</h3>
      <p>ވަކި ކަމެއް ވާނަމަ އެކަން ކުރުމަށް <code>ނަމަ</code> އަދި <code>ނޫންނަމަ</code> ބޭނުންކުރެއެވެ. ބްލޮކް ނިންމުމަށް <code>ނިމުނީ</code> ބޭނުންކުރަންވާނެއެވެ.</p>
      <pre><code>ނަމަ މާކްސް >= 50
    ދައްކާ "ފާސްވެއްޖެ"
ނޫންނަމަ
    ދައްކާ "ފާހެއްނުވި"
ނިމުނީ</code></pre>
    `,
    task: `<strong>މަސައްކަތް:</strong> <code>ނަމަ</code> ބޭނުންކޮށްގެން <code>އުމުރު >= 18</code> ނަމަ <code>"ބޮޑު މީހެއް"</code> ދައްކަވާ.`,
    initialCode: `ކަނޑައަޅާ އުމުރު = 20

ނަމަ އުމުރު >= 18
    ދައްކާ "ބޮޑު މީހެއް"
ނޫންނަމަ
    ދައްކާ "ކުޑަކުއްޖެއް"
ނިމުނީ
`,
    expectedMatch: /ބޮޑު މީހެއް/,
    hint: `ނަމަ އުމުރު >= 18 ބްލޮކް ފުރިހަމަކުރައްވާށެވެ.`
  },
  {
    id: 4,
    title: "4. ލޫޕްތައް (Loops)",
    subtitle: "ކަމެއް ތަކުރާރުކޮށް ހިންގުން",
    theory: `
      <h3>ހިނދު (While Loop)</h3>
      <p>ވަކި ޝަރުޠެއް ދެމިއޮތްހާ ހިނދަކު ކޯޑު ތަކުރާރުކުރުމަށް <code>ހިނދު</code> ބޭނުންކުރެވެއެވެ.</p>
      <pre><code>ކަނޑައަޅާ ގުނާ = 1
ހިނދު ގުނާ <= 3
    ދައްކާ "ގުނި އަދަދު: " + ގުނާ
    ކަނޑައަޅާ ގުނާ = ގުނާ + 1
ނިމުނީ</code></pre>
    `,
    task: `<strong>މަސައްކަތް:</strong> 1 ން 3 އަށް ނަންބަރުތައް ގުނައި ޓާމިނަލަށް ދައްކަވާ.`,
    initialCode: `ކަނޑައަޅާ ގުނާ = 1
ހިނދު ގުނާ <= 3
    ދައްކާ ގުނާ
    ކަނޑައަޅާ ގުނާ = ގުނާ + 1
ނިމުނީ
`,
    expectedMatch: /3/,
    hint: `ކަނޑައަޅާ ގުނާ = ގުނާ + 1 ލިޔުއްވައި 3 އާ ހަމައަށް ހިންގަވާ.`
  },
  {
    id: 5,
    title: "5. ލިސްޓާއި ރަދީފު",
    subtitle: "ގިނަ މަޢުލޫމާތު އެއްތަނެއްގައި ރައްކާކުރުން",
    theory: `
      <h3>ލިސްޓު އަދި ރަދީފު (Lists & Dictionaries)</h3>
      <p>ލިސްޓު: <code>["މާލެ", "ހުޅުމާލެ"]</code></p>
      <p>ރަދީފު (Key-Value): <code>{"ނަން": "ޢަލީ", "ރަށް": "މާލެ"}</code></p>
      <p><code>ކޮންމެ</code> ލޫޕުން ލިސްޓުގެ ތެރޭގައި ދަތުރުކުރެވެއެވެ.</p>
    `,
    task: `<strong>މަސައްކަތް:</strong> ރަދީފަކުން <code>"ނަން"</code> ނަގައިގެން ދައްކަވާ.`,
    initialCode: `ކަނޑައަޅާ ދަރިވަރު = {
    "ނަން": "މަރްޔަމް",
    "ގްރޭޑް": 10
}

ދައްކާ "ދަރިވަރުގެ ނަން: " + ދަރިވަރު["ނަން"]
`,
    expectedMatch: /މަރްޔަމް/,
    hint: `ދަރިވަރު["ނަން"] ބޭނުންކުރައްވާށެވެ.`
  },
  {
    id: 6,
    title: "6. ވަޒީފާތައް (Functions)",
    subtitle: "އަމިއްލަ ފަންކްޝަން ހެދުމާއި ބޭނުންކުރުން",
    theory: `
      <h3>ވަޒީފާ (Functions)</h3>
      <p>ތަކުރާރުކޮށް ބޭނުންކުރެވޭނެ ކޯޑު ބްލޮކެއް ހެދުމަށް <code>ވަޒީފާ</code> ބޭނުންކުރެއެވެ.</p>
      <pre><code>ވަޒީފާ ދެގުނަ(އަދަދު)
    ފޮނުވާ އަދަދު * 2
ނިމުނީ

ދައްކާ ދެގުނަ(7) // 14</code></pre>
    `,
    task: `<strong>މަސައްކަތް:</strong> <code>ގުނަކުރޭ(އޭ, ބީ)</code> ވަޒީފާއިން ދެ އަދަދު ގުނަކޮށް <code>5 * 6 = 30</code> ދައްކަވާ.`,
    initialCode: `ވަޒީފާ ގުނަކުރޭ(އޭ, ބީ)
    ފޮނުވާ އޭ * ބީ
ނިމުނީ

ކަނޑައަޅާ ޖަވާބު = ގުނަކުރޭ(5, 6)
ދައްކާ ޖަވާބު
`,
    expectedMatch: /30/,
    hint: `ގުނަކުރޭ(5, 6) ގޮވާލައްވާށެވެ.`
  },
  {
    id: 7,
    title: "7. ކުށް ސަލާމަތްކުރުން",
    subtitle: "ޕްރޮގްރާމް ނުހުއްޓި ރައްކާތެރިކުރުން",
    theory: `
      <h3>މަސައްކަތްކުރޭ ... ކުށެއް_ފެނިއްޖެނަމަ</h3>
      <p>ކޯޑެއް ހިންގާއިރު މައްސަލައެއް ޖެހިއްޖެނަމަ ޕްރޮގްރާމް ކްރޭޝް ނުވެ ސަލާމަތްކުރުމަށް މި ބްލޮކް ބޭނުންކުރެވެއެވެ.</p>
    `,
    task: `<strong>މަސައްކަތް:</strong> 0 އަށް ބަހަން އުޅުމުން ދިމާވާ ކުށް ސަލާމަތްކޮށް <code>"ކުށް ސަލާމަތްވެއްޖެ"</code> ދައްކަވާ.`,
    initialCode: `މަސައްކަތްކުރޭ
    ކަނޑައަޅާ ހިސާބު = 100 / 0
ކުށެއް_ފެނިއްޖެނަމަ މައްސަލަ
    ދައްކާ "ކުށް ސަލާމަތްވެއްޖެ: " + މައްސަލަ
ނިމުނީ
`,
    expectedMatch: /ކުށް ސަލާމަތްވެއްޖެ/,
    hint: `މަސައްކަތްކުރޭ އަދި ކުށެއް_ފެނިއްޖެނަމަ ބޭނުންކުރައްވާށެވެ.`
  },
  {
    id: 8,
    title: "8. ސަގާފީ މޮޑިއުލްތައް",
    subtitle: "ނަކަތާއި ނަމާދު ވަގުތުތައް ބޭނުންކުރުން",
    theory: `
      <h3>ދިވެހި ސަގާފީ ލައިބްރަރީތައް</h3>
      <p>ދިވެހި ކޯޑުގައި ހިމެނޭ މޮޑިއުލްތައް:</p>
      <ul>
        <li><code>ގެނޭ "ނަކަތް"</code>: ދިވެހި 27 ނަކަތުގެ މަޢުލޫމާތު.</li>
        <li><code>ގެނޭ "ނަމާދު"</code>: ރާއްޖޭގެ ރަށްރަށުގެ ނަމާދު ވަގުތުތައް.</li>
        <li><code>ގެނޭ "ތާނަ_ހިސާބު"</code>: އަދަދު ދިވެހި ބަހަށް ބަދަލުކުރުން (<code>އަދަދު_ބަހަށް</code>).</li>
      </ul>
    `,
    task: `<strong>މަސައްކަތް:</strong> <code>ތާނަ_ހިސާބު</code> ގެނެސް، <code>އަދަދު_ބަހަށް(125)</code> ދައްކަވާ (ނަތީޖާ: "ސަތޭކަ ފަންސަވީސް").`,
    initialCode: `ގެނޭ "ތާނަ_ހިސާބު"

ދައްކާ އަދަދު_ބަހަށް(125)
`,
    expectedMatch: /ސަތޭކަ ފަންސަވީސް/,
    hint: `ދައްކާ އަދަދު_ބަހަށް(125) ލިޔުއްވާށެވެ.`
  }
];

let currentLessonIndex = 0;
let completedLessons = JSON.parse(localStorage.getItem("dhicode_completed_lessons") || "[]");

// DOM Elements
const lessonListEl = document.getElementById("lesson-list");
const lessonTitleEl = document.getElementById("lesson-title");
const lessonSubtitleEl = document.getElementById("lesson-subtitle");
const lessonTheoryEl = document.getElementById("lesson-theory");
const lessonTaskEl = document.getElementById("lesson-task");
const editorEl = document.getElementById("code-editor");
const highlightEl = document.getElementById("code-highlight");
const highlightContentEl = document.getElementById("code-highlight-content");
const terminalEl = document.getElementById("terminal-output");
const btnRunEl = document.getElementById("btn-run");
const btnValidateEl = document.getElementById("btn-validate");
const btnResetEl = document.getElementById("btn-reset");
const btnPrevEl = document.getElementById("btn-prev-lesson");
const btnNextEl = document.getElementById("btn-next-lesson");
const progressTextEl = document.getElementById("progress-text");
const progressBarEl = document.getElementById("progress-bar-fill");

// Render lesson list
function renderLessonList() {
  if (!lessonListEl) return;
  lessonListEl.innerHTML = "";

  LESSONS.forEach((lesson, idx) => {
    const isCompleted = completedLessons.includes(lesson.id);
    const isActive = idx === currentLessonIndex;

    const item = document.createElement("button");
    item.className = `academy-lesson-item ${isActive ? "active" : ""} ${isCompleted ? "completed" : ""}`;
    item.innerHTML = `
      <div class="lesson-meta">
        <span class="lesson-badge">${isCompleted ? "✅" : (idx + 1)}</span>
        <div class="lesson-titles">
          <strong>${lesson.title}</strong>
          <small>${lesson.subtitle}</small>
        </div>
      </div>
    `;

    item.addEventListener("click", () => {
      loadLesson(idx);
    });

    lessonListEl.appendChild(item);
  });

  updateProgress();
}

// Update progress bar
function updateProgress() {
  const total = LESSONS.length;
  const count = completedLessons.length;
  const pct = Math.round((count / total) * 100);

  if (progressTextEl) progressTextEl.textContent = `${count} / ${total} ފުރިހަމަވެއްޖެ (${pct}%)`;
  if (progressBarEl) progressBarEl.style.width = `${pct}%`;
}

// Load a specific lesson
function loadLesson(idx) {
  if (idx < 0 || idx >= LESSONS.length) return;
  currentLessonIndex = idx;
  const lesson = LESSONS[idx];

  if (lessonTitleEl) lessonTitleEl.textContent = lesson.title;
  if (lessonSubtitleEl) lessonSubtitleEl.textContent = lesson.subtitle;
  if (lessonTheoryEl) lessonTheoryEl.innerHTML = lesson.theory;
  if (lessonTaskEl) lessonTaskEl.innerHTML = lesson.task;

  if (editorEl) {
    editorEl.value = lesson.initialCode;
    updateHighlight();
  }

  if (terminalEl) {
    terminalEl.innerHTML = '<div class="terminal-dim">ކޯޑު ހިންގުމަށް "▶ ހިންގާ" ފިއްތަވާ، ނުވަތަ ޓާސްކް ޗެކްކުރުމަށް "✨ ޗެކްކުރޭ" ފިއްތަވާ.</div>';
  }

  if (btnPrevEl) btnPrevEl.disabled = idx === 0;
  if (btnNextEl) btnNextEl.disabled = idx === LESSONS.length - 1;

  renderLessonList();
}

// Validate solution
async function validateSolution() {
  const lesson = LESSONS[currentLessonIndex];
  if (!lesson) return;

  btnValidateEl.disabled = true;
  btnValidateEl.textContent = "ޗެކްކުރަނީ...";

  await runDhiCode();

  const terminalText = terminalEl.textContent || "";
  const isMatch = lesson.expectedMatch.test(terminalText);

  if (isMatch) {
    if (!completedLessons.includes(lesson.id)) {
      completedLessons.push(lesson.id);
      localStorage.setItem("dhicode_completed_lessons", JSON.stringify(completedLessons));
    }
    renderLessonList();

    const banner = document.createElement("div");
    banner.className = "terminal-line terminal-success";
    banner.style.fontSize = "1.1rem";
    banner.style.marginTop = "10px";
    banner.innerHTML = `🎉 މަރުޙަބާ! މި ފިލާވަޅުގެ މަސައްކަތް ކާމިޔާބުކަމާއެކު ނިމިއްޖެ!`;
    terminalEl.appendChild(banner);
    terminalEl.scrollTop = terminalEl.scrollHeight;

    if (currentLessonIndex < LESSONS.length - 1) {
      setTimeout(() => {
        loadLesson(currentLessonIndex + 1);
      }, 1500);
    }
  } else {
    const banner = document.createElement("div");
    banner.className = "terminal-line terminal-error";
    banner.style.marginTop = "10px";
    banner.innerHTML = `❌ އަދި ނަތީޖާ ރަނގަޅެއް ނޫން. އިރުޝާދު: ${lesson.hint}`;
    terminalEl.appendChild(banner);
    terminalEl.scrollTop = terminalEl.scrollHeight;
  }

  btnValidateEl.disabled = false;
  btnValidateEl.textContent = "✨ ޗެކްކުރޭ (Validate)";
}

// Reset code
if (btnResetEl) {
  btnResetEl.addEventListener("click", () => {
    const lesson = LESSONS[currentLessonIndex];
    if (lesson && editorEl) {
      editorEl.value = lesson.initialCode;
      updateHighlight();
    }
  });
}

// Next / Prev buttons
if (btnPrevEl) {
  btnPrevEl.addEventListener("click", () => loadLesson(currentLessonIndex - 1));
}
if (btnNextEl) {
  btnNextEl.addEventListener("click", () => loadLesson(currentLessonIndex + 1));
}

// Validate button
if (btnValidateEl) {
  btnValidateEl.addEventListener("click", validateSolution);
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  renderLessonList();
  loadLesson(0);
});
