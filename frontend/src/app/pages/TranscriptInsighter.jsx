"use client";
import React, {useState} from 'react'
import TranscriptForm from '../components/TranscriptForm'
import Feed from '../components/Feed'

const TranscriptInsighter = () => {
  const [insight, setInsight] = useState(null)
  const [metadata, setMetadata] = useState(null)
  
  return (
    <div>
      <h1 className="text-3xl font-bold text-center mb-6">
        Transcript Insight App
      </h1>
      <TranscriptForm setInsight={setInsight} setMetadata={setMetadata} />
      <Feed insight={insight} metadata={metadata} />
    </div>
  )
}

export default TranscriptInsighter