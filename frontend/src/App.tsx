import { useState } from 'react';
import { UploadCloud, FileText, CheckCircle, AlertCircle, Briefcase, FileUp, Loader2 } from 'lucide-react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const [jobMatches, setJobMatches] = useState<any>(null);
  const [isLoadingJobs, setIsLoadingJobs] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setError(null);
    setResult(null);
    setJobMatches(null);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      // Point to backend API
      const response = await axios.post('http://localhost:8000/api/v1/cv/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
      
      // Immediately fetch job matches
      setIsLoadingJobs(true);
      try {
        const jobsResponse = await axios.post('http://localhost:8000/api/v1/jobs/match', response.data.data, {
          headers: { 'Content-Type': 'application/json' }
        });
        setJobMatches(jobsResponse.data);
      } catch (jobErr) {
        console.error("Failed to fetch jobs", jobErr);
      } finally {
        setIsLoadingJobs(false);
      }

    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || "An error occurred during CV analysis.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded bg-primary text-white flex items-center justify-center font-bold">
              AI
            </div>
            <h1 className="text-xl font-bold text-textPrimary tracking-tight">Career Analyzer</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {!result ? (
          // --- UPLOAD VIEW ---
          <div className="max-w-2xl mx-auto mt-12">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-textPrimary mb-3">Analyze your CV. Discover your best career paths.</h2>
              <p className="text-textSecondary text-lg">Upload your resume to get an instant ATS evaluation, discover your strengths, and find matching jobs in Sri Lanka.</p>
            </div>

            <div className="card p-8 text-center">
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-12 bg-gray-50 flex flex-col items-center justify-center transition-colors hover:border-primary">
                
                {isUploading ? (
                  <div className="flex flex-col items-center">
                    <Loader2 className="w-12 h-12 text-primary animate-spin mb-4" />
                    <h3 className="text-lg font-medium text-textPrimary">Analyzing CV...</h3>
                    <p className="text-textSecondary mt-2">Extracting skills and evaluating ATS compatibility</p>
                  </div>
                ) : (
                  <>
                    <UploadCloud className="w-16 h-16 text-gray-400 mb-4" />
                    <h3 className="text-lg font-medium text-textPrimary mb-1">Drag & drop your CV here</h3>
                    <p className="text-sm text-textSecondary mb-6">Supports PDF and DOCX</p>
                    
                    <input 
                      type="file" 
                      id="file-upload" 
                      className="hidden" 
                      accept=".pdf,.docx"
                      onChange={handleFileChange}
                    />
                    <label 
                      htmlFor="file-upload" 
                      className="btn-primary cursor-pointer inline-flex items-center gap-2"
                    >
                      <FileUp className="w-4 h-4" />
                      Browse Files
                    </label>
                  </>
                )}
              </div>
              
              {file && !isUploading && (
                <div className="mt-6 flex items-center justify-between bg-white border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center gap-3">
                    <FileText className="w-6 h-6 text-primary" />
                    <div className="text-left">
                      <p className="text-sm font-medium text-textPrimary">{file.name}</p>
                      <p className="text-xs text-textSecondary">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                    </div>
                  </div>
                  <button onClick={handleUpload} className="btn-primary">
                    Analyze CV
                  </button>
                </div>
              )}
              
              {error && (
                <div className="mt-6 flex items-center gap-2 text-red-600 bg-red-50 p-4 rounded-lg">
                  <AlertCircle className="w-5 h-5 flex-shrink-0" />
                  <p className="text-sm text-left">{error}</p>
                </div>
              )}
            </div>

            <div className="mt-6 flex items-center justify-center gap-2 text-sm text-textSecondary">
              <CheckCircle className="w-4 h-4 text-green-500" />
              <span><strong>Privacy First:</strong> Your CV is processed temporarily in memory and is automatically deleted after analysis. It is never stored.</span>
            </div>
          </div>
        ) : (
          // --- RESULTS VIEW ---
          <div>
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-2xl font-bold text-textPrimary">Your Analysis Results</h2>
              <button onClick={() => {setResult(null); setFile(null);}} className="text-primary font-medium hover:underline">
                Analyze another CV
              </button>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Left Column: ATS Score & Profile */}
              <div className="space-y-6">
                <div className="card text-center relative overflow-hidden">
                  <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-purple-500"></div>
                  <h3 className="text-lg font-medium text-textSecondary mb-2">Overall ATS Score</h3>
                  <div className="text-6xl font-bold text-textPrimary my-4">
                    {result.data?.ats_analysis?.overall_score || '--'}
                    <span className="text-2xl text-gray-400">/100</span>
                  </div>
                  <p className="text-sm text-textSecondary">
                    Based on keyword optimization, structure, and readability.
                  </p>
                </div>
                
                <div className="card">
                  <h3 className="text-lg font-bold text-textPrimary mb-4">Candidate Profile</h3>
                  <div className="space-y-3">
                    <p><strong>Name:</strong> {result.data?.candidate?.name || 'Not found'}</p>
                    <p><strong>Email:</strong> {result.data?.candidate?.email || 'Not found'}</p>
                    <p><strong>Location:</strong> {result.data?.candidate?.location || 'Not found'}</p>
                  </div>
                  
                  <div className="mt-6">
                    <h4 className="text-sm font-semibold text-textSecondary uppercase tracking-wider mb-3">Top Skills</h4>
                    <div className="flex flex-wrap gap-2">
                      {result.data?.technical_skills?.map((skill: str, i: number) => (
                        <span key={i} className="px-3 py-1 bg-indigo-50 text-primary text-sm font-medium rounded-full">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Column: Strengths & Weaknesses */}
              <div className="lg:col-span-2 space-y-6">
                
                <div className="card">
                  <h3 className="text-xl font-bold text-textPrimary mb-4">Top Strengths</h3>
                  <div className="space-y-4">
                    {result.data?.strengths?.map((strength: any, i: number) => (
                      <div key={i} className="flex gap-4 p-4 border border-gray-100 rounded-lg bg-gray-50">
                        <div className="w-8 h-8 rounded-full bg-green-100 text-green-600 flex items-center justify-center flex-shrink-0 font-bold">
                          {i + 1}
                        </div>
                        <div>
                          <h4 className="font-bold text-textPrimary">{strength.title}</h4>
                          <p className="text-textSecondary text-sm mt-1">{strength.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="card">
                  <h3 className="text-xl font-bold text-textPrimary mb-4">Improvement Roadmap</h3>
                  <div className="space-y-4">
                    {result.data?.improvement_areas?.map((area: any, i: number) => (
                      <div key={i} className="p-4 border border-gray-100 rounded-lg bg-white relative overflow-hidden">
                        <div className={`absolute top-0 left-0 w-1 h-full ${area.priority.includes('HIGH') ? 'bg-red-500' : 'bg-yellow-400'}`}></div>
                        <div className="pl-3">
                          <div className="flex justify-between items-start mb-2">
                            <h4 className="font-bold text-textPrimary">Skill Gap: {area.skill}</h4>
                            <span className={`text-xs font-bold px-2 py-1 rounded-full ${area.priority.includes('HIGH') ? 'bg-red-50 text-red-600' : 'bg-yellow-50 text-yellow-600'}`}>
                              {area.priority}
                            </span>
                          </div>
                          <p className="text-sm text-textSecondary mb-2"><strong>Status:</strong> {area.status}</p>
                          <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded">{area.recommendation}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

              </div>
            </div>
            
            {/* Roles and Jobs Section */}
            <div className="mt-8">
              <h2 className="text-2xl font-bold text-textPrimary mb-6">Career Matches & Jobs</h2>
              
              {isLoadingJobs ? (
                <div className="card flex flex-col items-center justify-center p-12">
                  <Loader2 className="w-10 h-10 text-primary animate-spin mb-4" />
                  <p className="text-textSecondary">Finding the best roles and jobs for you...</p>
                </div>
              ) : jobMatches ? (
                <div className="space-y-8">
                  
                  {/* Top Roles */}
                  <div>
                    <h3 className="text-xl font-bold text-textPrimary mb-4">Recommended Roles</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      {jobMatches.roles.map((role: any, i: number) => (
                        <div key={i} className="card border-l-4 border-l-primary">
                          <div className="flex justify-between items-start mb-2">
                            <h4 className="font-bold text-textPrimary">{role.title}</h4>
                            <span className="bg-green-100 text-green-700 text-xs font-bold px-2 py-1 rounded-full">
                              {role.match_score}% Match
                            </span>
                          </div>
                          <p className="text-sm text-textSecondary mb-3">{role.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Top Jobs */}
                  <div>
                    <h3 className="text-xl font-bold text-textPrimary mb-4">Available Jobs in Sri Lanka</h3>
                    <div className="space-y-4">
                      {jobMatches.jobs.length > 0 ? jobMatches.jobs.map((job: any) => (
                        <div key={job.id} className="card flex flex-col md:flex-row md:items-center justify-between gap-4">
                          <div>
                            <div className="flex items-center gap-3 mb-1">
                              <h4 className="font-bold text-lg text-textPrimary">{job.title}</h4>
                              <span className={`text-xs font-bold px-2 py-1 rounded-full ${job.match_score >= 80 ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
                                {job.match_score}% Match
                              </span>
                            </div>
                            <p className="text-sm text-textSecondary font-medium">{job.company} • {job.location}</p>
                            <div className="flex flex-wrap gap-2 mt-3">
                              {job.match_reasons.map((skill: string, idx: number) => (
                                <span key={idx} className="text-xs bg-indigo-50 text-primary px-2 py-1 rounded">{skill}</span>
                              ))}
                              {job.missing_skills.slice(0,3).map((skill: string, idx: number) => (
                                <span key={idx} className="text-xs bg-red-50 text-red-500 px-2 py-1 rounded line-through">{skill}</span>
                              ))}
                            </div>
                          </div>
                          <div className="flex flex-col items-end gap-2 shrink-0">
                            <span className="text-sm font-bold text-gray-700">{job.salary_range}</span>
                            <a href={job.url} target="_blank" rel="noreferrer" className="btn-primary text-sm px-4 py-2">
                              Apply Now
                            </a>
                          </div>
                        </div>
                      )) : (
                        <div className="p-8 text-center bg-gray-50 rounded-lg border border-gray-200">
                          <p className="text-textSecondary">No matching jobs found for your profile at this time.</p>
                        </div>
                      )}
                    </div>
                  </div>

                </div>
              ) : null}
            </div>

          </div>
        )}
      </main>
    </div>
  );
}

export default App;
