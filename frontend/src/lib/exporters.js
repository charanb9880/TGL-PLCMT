const escapeCell = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;


const downloadCsv = (filename, rows) => {
  const blob = new Blob([rows.join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
};


export const exportFilteredCompaniesCsv = (companies = []) => {
  const headers = [
    "Company Name",
    "Category",
    "Employee Size",
    "Focus Sectors / Industries",
    "Hiring Velocity",
    "Profitability Status",
  ];
  const rows = [headers.map(escapeCell).join(",")];
  companies.forEach((company) => {
    rows.push(headers.map((header) => escapeCell(company[header])).join(","));
  });
  downloadCsv("filtered-company-list.csv", rows);
};


export const exportComparisonCsv = (comparison, sections) => {
  if (!comparison) {
    return;
  }

  const rows = [["Section", "Field", comparison.left_company?.["Company Name"], comparison.right_company?.["Company Name"]].map(escapeCell).join(",")];
  sections.forEach((section) => {
    section.fields.forEach((field) => {
      rows.push([
        escapeCell(section.title),
        escapeCell(field),
        escapeCell(comparison.left_company?.[field]),
        escapeCell(comparison.right_company?.[field]),
      ].join(","));
    });
  });

  downloadCsv("company-comparison.csv", rows);
};


export const exportFacultyBriefingCsv = ({ analytics, companies = [], comparison }) => {
  const rows = [];

  rows.push(["Faculty Briefing Pack"].map(escapeCell).join(","));
  rows.push([escapeCell("Total companies"), escapeCell(analytics?.total_companies || companies.length)].join(","));
  rows.push([escapeCell("Top categories"), escapeCell((analytics?.category_distribution || []).slice(0, 3).map((item) => `${item.label} (${item.value})`).join(" | "))].join(","));
  rows.push([escapeCell("Top hiring velocity bands"), escapeCell((analytics?.hiring_velocity_distribution || []).slice(0, 3).map((item) => `${item.label} (${item.value})`).join(" | "))].join(","));
  rows.push("");

  rows.push(["Top Companies"].map(escapeCell).join(","));
  rows.push(["Company Name", "Category", "Employee Size", "Hiring Velocity", "Profitability Status"].map(escapeCell).join(","));
  companies.slice(0, 5).forEach((company) => {
    rows.push([
      escapeCell(company["Company Name"]),
      escapeCell(company.Category),
      escapeCell(company["Employee Size"]),
      escapeCell(company["Hiring Velocity"]),
      escapeCell(company["Profitability Status"]),
    ].join(","));
  });

  rows.push("");
  rows.push(["Filtered Company List"].map(escapeCell).join(","));
  rows.push(["Company Name", "Category", "Employee Size", "Focus Sectors / Industries", "Hiring Velocity", "Profitability Status"].map(escapeCell).join(","));
  companies.forEach((company) => {
    rows.push([
      escapeCell(company["Company Name"]),
      escapeCell(company.Category),
      escapeCell(company["Employee Size"]),
      escapeCell(company["Focus Sectors / Industries"]),
      escapeCell(company["Hiring Velocity"]),
      escapeCell(company["Profitability Status"]),
    ].join(","));
  });

  rows.push("");
  rows.push(["Comparison Snapshot"].map(escapeCell).join(","));
  rows.push([escapeCell("Left Company"), escapeCell(comparison?.left_company?.["Company Name"] || "Not included")].join(","));
  rows.push([escapeCell("Right Company"), escapeCell(comparison?.right_company?.["Company Name"] || "Not included")].join(","));

  downloadCsv("faculty-briefing-pack.csv", rows);
};


export const openFacultyPdfReport = ({ title, description = "", analytics, companies = [], comparison }) => {
  const printWindow = window.open("", "_blank", "noopener,noreferrer");
  if (!printWindow) {
    return;
  }

  const companyRows = companies.map((company) => `
    <tr>
      <td>${company["Company Name"] || ""}</td>
      <td>${company.Category || ""}</td>
      <td>${company["Employee Size"] || ""}</td>
      <td>${company["Hiring Velocity"] || ""}</td>
      <td>${company["Profitability Status"] || ""}</td>
    </tr>
  `).join("");

  printWindow.document.write(`
    <html>
      <head>
        <title>${title}</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 32px; color: #111827; }
          h1 { margin-bottom: 4px; }
          p { color: #4b5563; line-height: 1.6; }
          .grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; margin: 24px 0; }
          .card { border: 1px solid #e5e7eb; border-radius: 16px; padding: 16px; }
          table { width: 100%; border-collapse: collapse; margin-top: 18px; }
          th, td { border: 1px solid #e5e7eb; padding: 10px; text-align: left; font-size: 12px; }
          th { background: #f9fafb; }
        </style>
      </head>
      <body>
        <h1>${title}</h1>
        <p>${description}</p>
        <div class="grid">
          <div class="card"><strong>Total companies</strong><div>${analytics?.total_companies || companies.length}</div></div>
          <div class="card"><strong>Top categories</strong><div>${(analytics?.category_distribution || []).slice(0, 3).map((item) => `${item.label} (${item.value})`).join(" · ")}</div></div>
          <div class="card"><strong>Hiring signals</strong><div>${(analytics?.hiring_velocity_distribution || []).slice(0, 3).map((item) => `${item.label} (${item.value})`).join(" · ")}</div></div>
        </div>
        <h2>Company summaries</h2>
        <table>
          <thead>
            <tr><th>Company Name</th><th>Category</th><th>Employee Size</th><th>Hiring Velocity</th><th>Profitability Status</th></tr>
          </thead>
          <tbody>${companyRows}</tbody>
        </table>
        <h2>Comparison snapshot</h2>
        <p>Left company: ${comparison?.left_company?.["Company Name"] || "Not included"}</p>
        <p>Right company: ${comparison?.right_company?.["Company Name"] || "Not included"}</p>
        <script>window.onload = () => window.print()</script>
      </body>
    </html>
  `);
  printWindow.document.close();
};