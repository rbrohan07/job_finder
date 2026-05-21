import { useState } from "react";
import axios from "axios";

export default function App() {
  const [formData, setFormData] = useState({
    query: "",
    expected_salary: "",
    location: "",
    results_wanted: 20,
    country: "india",
    selected_sources: ["remoteio", "remoteok"],
  });
  const AVAILABLE_SOURCES = [
    "remoteio",
    "remoteok",
    "indeed",
    "linkedin",
    "zip_recruiter",
    "glassdoor",
    "google",
    "naukri",
    "bayt",
    "bdjobs",
  ];

  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  //for source selection
  const handleSourceChange = (source) => {
    setFormData((prev) => {
      const alreadySelected = prev.selected_sources.includes(source);

      return {
        ...prev,
        selected_sources: alreadySelected
          ? prev.selected_sources.filter((s) => s !== source)
          : [...prev.selected_sources, source],
      };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/search-jobs",
        formData,
      );

      setJobs(response.data);
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>AI Job Search</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="query"
          placeholder="Job role"
          onChange={handleChange}
        />

        <br />
        <br />

        <input
          type="text"
          name="location"
          placeholder="Location"
          onChange={handleChange}
        />

        <br />
        <br />

        <input
          type="number"
          name="expected_salary"
          placeholder="Expected Salary"
          onChange={handleChange}
        />

        <h3>Select Platforms</h3>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: "10px",
            marginBottom: "20px",
          }}
        >
          {AVAILABLE_SOURCES.map((source) => (
            <label key={source}>
              <input
                type="checkbox"
                checked={formData.selected_sources.includes(source)}
                onChange={() => handleSourceChange(source)}
              />{" "}
              {source}
            </label>
          ))}
        </div>
        <br />
        <br />

        <button type="submit">Search Jobs</button>
      </form>

      <br />

      {loading && <h2>Loading...</h2>}

      {jobs.map((job) => (
        <div
          key={job.id}
          style={{
            border: "1px solid gray",
            padding: "15px",
            marginBottom: "10px",
            borderRadius: "10px",
          }}
        >
          <h2>{job.title}</h2>

          <p>
            <b>Company:</b> {job.company}
          </p>

          <p>
            <b>Location:</b> {job.location}
          </p>

          <p>
            <b>Score:</b> {job.total_score}
          </p>

          <p>
            <b>Source:</b> {job.source}
          </p>

          <a href={job.job_url} target="_blank">
            Apply
          </a>
        </div>
      ))}
    </div>
  );
}
