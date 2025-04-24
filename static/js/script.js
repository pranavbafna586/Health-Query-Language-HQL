// Health Query Language (HQL) Web Interface JavaScript
document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const queryInput = document.getElementById("query-input");
  const executeBtn = document.getElementById("execute-btn");
  const clearBtn = document.getElementById("clear-btn");
  const exampleQueriesContainer = document.getElementById("example-queries");
  const resultsContainer = document.getElementById("results-container");
  const totalPatientsEl = document.getElementById("total-patients");
  const ageDistributionEl = document.getElementById("age-distribution");
  const genderDistributionEl = document.getElementById("gender-distribution");
  const medicalConditionsEl = document.getElementById("medical-conditions");

  // Load example queries
  loadExampleQueries();

  // Load patient statistics
  loadPatientStats();

  // After loading static sample grid items, attach click handlers
  document.querySelectorAll(".sample-item").forEach((item) => {
    item.addEventListener("click", () => {
      queryInput.value = item.textContent.trim();
      queryInput.focus();
    });
  });

  // Event Handlers
  executeBtn.addEventListener("click", executeQuery);
  clearBtn.addEventListener("click", clearQuery);

  function executeQuery() {
    const query = queryInput.value.trim();

    if (!query) {
      showError("Please enter a query");
      return;
    }

    // Show loading spinner
    resultsContainer.innerHTML =
      '<div class="text-center"><div class="spinner"></div><p>Executing query...</p></div>';

    // Execute the query
    const formData = new FormData();
    formData.append("query", query);

    fetch("/execute", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          showError(data.error);
          return;
        }

        displayResults(data);
      })
      .catch((error) => {
        showError("An error occurred while executing the query");
        console.error(error);
      });
  }

  function clearQuery() {
    queryInput.value = "";
    queryInput.focus();
  }

  function loadExampleQueries() {
    fetch("/examples")
      .then((response) => response.json())
      .then((examples) => {
        exampleQueriesContainer.innerHTML = "";

        examples.forEach((example) => {
          const exampleEl = document.createElement("div");
          exampleEl.className = "example-query";
          exampleEl.innerHTML = `
                        <h4>${example.title}</h4>
                        <p>${example.description}</p>
                        <code>${example.query}</code>
                    `;

          // Add click event to populate query input
          exampleEl.addEventListener("click", () => {
            queryInput.value = example.query;
            queryInput.focus();
          });

          exampleQueriesContainer.appendChild(exampleEl);
        });
      })
      .catch((error) => {
        console.error("Failed to load example queries:", error);
        exampleQueriesContainer.innerHTML =
          "<p>Failed to load example queries</p>";
      });
  }

  function loadPatientStats() {
    fetch("/patient-stats")
      .then((response) => response.json())
      .then((stats) => {
        // Update the stats display
        totalPatientsEl.textContent = stats.total_patients;

        const ageStats = stats.age_distribution;
        ageDistributionEl.textContent = `Min: ${ageStats.min} | Avg: ${ageStats.avg} | Max: ${ageStats.max}`;

        const genderStats = stats.gender_distribution;
        genderDistributionEl.innerHTML = `
                    Male: <strong>${genderStats.M || 0}</strong> | 
                    Female: <strong>${genderStats.F || 0}</strong>
                `;

        const conditions = stats.conditions;
        medicalConditionsEl.innerHTML = `
                    Diabetes: <strong>${conditions.diabetes}</strong> | 
                    Hypertension: <strong>${conditions.hypertension}</strong> | 
                    Asthma: <strong>${conditions.asthma}</strong>
                `;
      })
      .catch((error) => {
        console.error("Failed to load patient statistics:", error);
      });
  }

  function displayResults(data) {
    switch (data.command) {
      case "find":
        displayFindResults(data);
        break;
      case "show":
        displayShowResults(data);
        break;
      case "alert":
        displayAlertResults(data);
        break;
      default:
        showError("Unknown command type");
    }
  }

  function displayFindResults(data) {
    if (data.count === 0) {
      resultsContainer.innerHTML = `
                <div class="result-summary">
                    <p>No patients found matching your criteria.</p>
                </div>
            `;
      return;
    }

    // Create a table to display patient data
    const patients = data.data;

    // Get all columns from the first patient
    const columns = Object.keys(patients[0]);

    let tableHTML = `
            <div class="result-summary">
                <p>Found ${data.count} patient(s) matching your criteria.</p>
            </div>
            <div class="result-find">
                <table>
                    <thead>
                        <tr>
                            ${columns.map((col) => `<th>${col}</th>`).join("")}
                        </tr>
                    </thead>
                    <tbody>
        `;

    // Add rows for each patient
    patients.forEach((patient) => {
      tableHTML += "<tr>";
      columns.forEach((col) => {
        tableHTML += `<td>${patient[col]}</td>`;
      });
      tableHTML += "</tr>";
    });

    tableHTML += `
                    </tbody>
                </table>
            </div>
        `;

    resultsContainer.innerHTML = tableHTML;
  }

  function displayShowResults(data) {
    resultsContainer.innerHTML = `
            <div class="result-show">
                <div class="result-label">${data.function.toUpperCase()} of ${
      data.attribute
    }</div>
                <div class="result-value">${data.result}</div>
                <p>Calculated from ${data.count} patient(s)</p>
            </div>
        `;
  }

  function displayAlertResults(data) {
    if (data.alert_triggered) {
      resultsContainer.innerHTML = `
                <div class="result-alert">
                    <div class="alert-icon"><i class="fas fa-exclamation-triangle"></i></div>
                    <div class="alert-triggered">ALERT TRIGGERED!</div>
                    <p>${data.matching_patients} patient(s) match alert condition</p>
                </div>
            `;
    } else {
      resultsContainer.innerHTML = `
                <div class="result-alert">
                    <div class="alert-icon" style="color: var(--success-color)"><i class="fas fa-check-circle"></i></div>
                    <div class="alert-safe">No alerts triggered</div>
                    <p>All patients are within safe parameters</p>
                </div>
            `;
    }
  }

  function showError(message) {
    resultsContainer.innerHTML = `
            <div class="error-message">
                <strong>Error:</strong> ${message}
            </div>
        `;
  }
});
