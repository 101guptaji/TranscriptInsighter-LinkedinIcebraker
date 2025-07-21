"use client";
import React, {useState} from 'react'
import TranscriptForm from '../components/TranscriptForm'
import Feed from '../components/Feed'

const TranscriptInsighter = () => {
  const [insight, setInsight] = useState(null)
  const [metadata, setMetadata] = useState(null)
  
  return (
    <div className='w-1/2 mx-auto p-6 bg-white rounded shadow'>
      <h1 className="text-3xl font-bold text-center mb-6">
        Transcript Insighter
      </h1>
      <TranscriptForm setInsight={setInsight} setMetadata={setMetadata} />
      <Feed insight={insight} metadata={metadata} />
    </div>
  )
}

export default TranscriptInsighter