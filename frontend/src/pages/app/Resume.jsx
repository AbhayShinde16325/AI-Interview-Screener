import { useCallback, useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import Button from '../../components/ui/Button'
import Badge from '../../components/ui/Badge'
import Skeleton from '../../components/ui/Skeleton'
import Alert from '../../components/ui/Alert'
import EmptyState from '../../components/ui/EmptyState'
import { getLatestResume, getParsedResumeDetails, uploadResume } from '../../services/resumes'
import { friendlyError } from '../../utils/errors'

function ProfileSection({ title, items, renderItem, emptyNote, aside }) {
  return (
    <section className="overflow-hidden rounded-lg border border-ink-200 bg-white shadow-card">
      <div className="flex items-center justify-between border-b border-ink-100 px-5 py-4">
        <h3 className="text-sm font-semibold text-ink-900">{title}</h3>
        {aside}
      </div>
      {items && items.length > 0 ? (
        <div className="divide-y divide-ink-100">{items.map(renderItem)}</div>
      ) : (
        <p className="px-5 py-6 text-sm text-ink-400">{emptyNote}</p>
      )}
    </section>
  )
}

function UploadDropzone({ onUploaded }) {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef(null)

  const handleUpload = async () => {
    if (!file) return
    setError('')
    setUploading(true)
    try {
      await uploadResume(file)
      setFile(null)
      if (inputRef.current) inputRef.current.value = ''
      onUploaded()
    } catch (err) {
      setError(friendlyError(err, 'Upload failed. Make sure the file is a valid PDF.'))
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="rounded-lg border border-ink-200 bg-white p-6 shadow-card">
      <div
        role="button"
        tabIndex={0}
        aria-label="Choose a PDF resume to upload"
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') inputRef.current?.click()
        }}
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragging(false)
          const dropped = e.dataTransfer.files?.[0]
          if (dropped) setFile(dropped)
        }}
        className={`cursor-pointer rounded-lg border-2 border-dashed px-6 py-10 text-center transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-600/40 ${
          dragging ? 'border-brand-400 bg-brand-50/50' : 'border-ink-300 hover:border-brand-400'
        }`}
      >
        <svg className="mx-auto h-8 w-8 text-ink-300" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6z" />
          <path d="M11 2.5V6a1 1 0 001 1h3.5L11 2.5z" />
        </svg>
        <p className="mt-3 text-sm font-medium text-ink-800">
          {file ? file.name : 'Drop your resume here, or click to browse'}
        </p>
        <p className="mt-1 text-[13px] text-ink-400">PDF up to 10 MB</p>
      </div>

      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        className="sr-only"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      {error && <Alert className="mt-4">{error}</Alert>}

      {file && (
        <div className="mt-4 flex justify-end">
          <Button onClick={handleUpload} loading={uploading} loadingText="Analyzing resume…">
            Upload &amp; analyze
          </Button>
        </div>
      )}
    </div>
  )
}

export default function Resume() {
  const [resume, setResume] = useState(null)
  const [details, setDetails] = useState(null)
  const [missing, setMissing] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [justUploaded, setJustUploaded] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      try {
        const res = await getLatestResume()
        setResume(res.data)
      } catch (err) {
        if (err.response?.status === 404) {
          setMissing(true)
        } else {
          throw err
        }
      }

      // Isolated call — currently returns null (see services/resumes.js).
      const parsed = await getParsedResumeDetails()
      setDetails(parsed)
    } catch (err) {
      setError(friendlyError(err, 'Failed to load your resume.'))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load])

  const handleUploaded = () => {
    setJustUploaded(true)
    load()
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-40 w-full" />
        <Skeleton className="h-48 w-full" />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-ink-900">Your resume</h1>
          <p className="mt-1 text-sm text-ink-500">
            The interview is built from the information below.
          </p>
        </div>
        {resume && (
          <Link to="/app/interviews/new">
            <Button>Start an interview</Button>
          </Link>
        )}
      </header>

      {error && <Alert>{error}</Alert>}

      {justUploaded && (
        <Alert tone="success" title="Resume uploaded and parsed">
          Your skills are ready. You can start an interview now.
        </Alert>
      )}

      {!missing && resume && (
        <section className="rounded-lg border border-ink-200 bg-white p-5 shadow-card">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-ink-50 text-ink-400">
                <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6z" />
                  <path d="M11 2.5V6a1 1 0 001 1h3.5L11 2.5z" />
                </svg>
              </span>
              <div>
                <p className="font-medium text-ink-900">{resume.filename}</p>
                <p className="text-[13px] text-ink-500">
                  Uploaded {new Date(resume.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
            <Badge tone="green" dot>
              Parsed
            </Badge>
          </div>

          <div className="mt-5 flex justify-end border-t border-ink-100 pt-4">
            <label className="inline-flex h-10 cursor-pointer items-center justify-center rounded-lg border border-ink-300 bg-white px-4 text-sm font-medium text-ink-800 transition-colors hover:border-ink-400 hover:bg-ink-50 focus-within:outline-none focus-within:ring-2 focus-within:ring-brand-600/40">
              Upload new resume
              <input
                type="file"
                accept="application/pdf"
                className="sr-only"
                onChange={(e) => {
                  const file = e.target.files?.[0]
                  if (!file) return
                  uploadResume(file)
                    .then(() => {
                      setJustUploaded(true)
                      load()
                    })
                    .catch((err) => setError(friendlyError(err, 'Upload failed.')))
                  e.target.value = ''
                }}
              />
            </label>
          </div>
        </section>
      )}

      {missing && (
        <>
          <div className="mb-6">
            <UploadDropzone onUploaded={handleUploaded} />
          </div>
          <EmptyState
            title="No resume uploaded yet"
            description="Upload your resume above to create a personalized interview."
            action={
              <Link to="/app/interviews/new">
                <Button variant="secondary">Browse interviews</Button>
              </Link>
            }
          />
        </>
      )}

      {resume && (
        <div className="grid gap-6">
          {/* Summary */}
          <section className="rounded-lg border border-ink-200 bg-white p-5 shadow-card">
            <h3 className="text-sm font-semibold text-ink-900">Summary</h3>
            {resume.summary ? (
              <p className="mt-2 text-sm leading-relaxed text-ink-600">{resume.summary}</p>
            ) : (
              <p className="mt-2 text-sm text-ink-400">No summary available.</p>
            )}
          </section>

          {/* Skills */}
          <section className="rounded-lg border border-ink-200 bg-white p-5 shadow-card">
            <h3 className="text-sm font-semibold text-ink-900">Skills</h3>
            {resume.skills.length > 0 ? (
              <div className="mt-3 flex flex-wrap gap-2">
                {resume.skills.map((skill) => (
                  <Badge key={skill} tone="blue" className="px-3 py-1">
                    {skill}
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="mt-2 text-sm text-ink-400">No skills detected.</p>
            )}
          </section>

          {/* Detailed profile — rendered from the isolated future endpoint */}
          <ProfileSection
            title="Education"
            items={details?.education || null}
            emptyNote="Detailed education will appear here once the full parsed profile is available."
            renderItem={(item, i) => (
              <div key={i} className="px-5 py-4">
                <p className="font-medium text-ink-900">{item.degree}</p>
                <p className="text-sm text-ink-500">
                  {item.institution}
                  {item.graduation_year ? ` · ${item.graduation_year}` : ''}
                </p>
              </div>
            )}
          />

          <ProfileSection
            title="Experience"
            items={details?.experience || null}
            emptyNote="Work experience will appear here once the full parsed profile is available."
            renderItem={(item, i) => (
              <div key={i} className="px-5 py-4">
                <p className="font-medium text-ink-900">{item.role}</p>
                <p className="text-sm text-ink-500">
                  {item.company} · {item.duration}
                </p>
              </div>
            )}
          />

          <ProfileSection
            title="Projects"
            items={details?.projects || null}
            emptyNote="Your projects will appear here once the full parsed profile is available."
            renderItem={(item, i) => (
              <div key={i} className="px-5 py-4">
                <p className="font-medium text-ink-900">{item.title}</p>
                {item.description && (
                  <p className="mt-1 text-sm leading-relaxed text-ink-500">{item.description}</p>
                )}
                {item.technologies?.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {item.technologies.map((tech) => (
                      <Badge key={tech} tone="neutral" className="px-2">
                        {tech}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            )}
          />

          <ProfileSection
            title="Certifications"
            items={details?.certifications || null}
            emptyNote="Certifications will appear here once the full parsed profile is available."
            renderItem={(item, i) => (
              <div key={i} className="px-5 py-4">
                <p className="text-sm font-medium text-ink-800">{item}</p>
              </div>
            )}
          />
        </div>
      )}
    </div>
  )
}
