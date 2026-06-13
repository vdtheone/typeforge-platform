'use client';
import { useEffect, useRef, useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { generateWords, generateQuote } from '@/utils/words';
import { api, useAuthStore } from '@/utils/api';
import { RotateCcw, Clock, Hash, ShieldAlert, ChevronRight, Quote, Type, Mountain, Wrench, Globe } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
} from 'recharts';

type TestMode = 'time' | 'words' | 'quote';

export default function TypingEngine() {
  // Config State
  const [mode, setMode] = useState<TestMode>('time');
  const [modeValue, setModeValue] = useState<number>(30); // e.g., 30s or 30 words
  const [usePunctuation, setUsePunctuation] = useState(false);
  const [useNumbers, setUseNumbers] = useState(false);

  // DOM Refs
  const inputRef = useRef<HTMLInputElement>(null);
  const wordsContainerRef = useRef<HTMLDivElement>(null);

  // Core State
  const [words, setWords] = useState<string[]>([]);
  const [typedInput, setTypedInput] = useState<string>('');
  const [history, setHistory] = useState<string[]>([]);
  
  // Game State
  const [status, setStatus] = useState<'idle' | 'running' | 'finished'>('idle');
  const [timeLeft, setTimeLeft] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  
  // Stats
  const [stats, setStats] = useState({ wpm: 0, raw: 0, accuracy: 0, correctChars: 0, incorrectChars: 0, extraChars: 0, missedChars: 0 });
  const [chartData, setChartData] = useState<any[]>([]);
  const [scrollOffset, setScrollOffset] = useState(0);

  // Initialize test
  const resetTest = () => {
    if (mode === 'quote') {
      const quoteWords = generateQuote();
      setWords(quoteWords);
      setTimeLeft(0);
    } else {
      const initialWordCount = mode === 'words' ? modeValue : 100;
      setWords(generateWords(initialWordCount, { punctuation: usePunctuation, numbers: useNumbers }));
      setTimeLeft(mode === 'time' ? modeValue : 0);
    }
    
    setTypedInput('');
    setHistory([]);
    setStatus('idle');
    setStartTime(null);
    setScrollOffset(0);
    setStats({ wpm: 0, raw: 0, accuracy: 0, correctChars: 0, incorrectChars: 0, extraChars: 0, missedChars: 0 });
    setChartData([]);
    setTimeout(() => inputRef.current?.focus(), 100);
  };

  // Handle Mode changes
  useEffect(() => {
    resetTest();
  }, [mode, modeValue, usePunctuation, useNumbers]);

  // Main game loop (Timer strictly for counting)
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (status === 'running') {
      interval = setInterval(() => {
        if (mode === 'time') {
          setTimeLeft((t) => Math.max(0, t - 1));
        } else {
          // Words mode just counts time up
          setTimeLeft((t) => t + 1);
        }
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [status, mode]);

  // Handle Game Over and Chart Recording on tick
  useEffect(() => {
    if (status === 'running') {
      if (mode === 'time' && timeLeft === 0) {
        finishTest();
      } else {
        recordChartData();
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeLeft, status, mode]);

  // Focus management
  useEffect(() => {
    const handleGlobalClick = () => {
      if (status !== 'finished') inputRef.current?.focus();
    };
    document.addEventListener('click', handleGlobalClick);
    return () => document.removeEventListener('click', handleGlobalClick);
  }, [status]);

  // Smooth line scrolling logic
  useEffect(() => {
    const container = wordsContainerRef.current;
    const currentIndex = history.length;
    if (container && container.children[currentIndex]) {
      const activeWordEl = container.children[currentIndex] as HTMLElement;
      const offsetTop = activeWordEl.offsetTop;
      
      const firstWordEl = container.children[0] as HTMLElement;
      if (firstWordEl) {
        // Height of one line (using standard line height without vertical gaps)
        const rowHeight = firstWordEl.offsetHeight;
        
        let newOffset = 0;
        if (offsetTop > rowHeight * 0.5) { 
           newOffset = offsetTop - rowHeight;
        }
        if (newOffset < 0) newOffset = 0;
        
        setScrollOffset(newOffset);
      }
    } else if (currentIndex === 0) {
      setScrollOffset(0);
    }
  }, [history.length, words]);

  const finishTest = () => {
    setStatus('finished');
    calculateFinalStats();
  };

  const calculateCurrentMetrics = () => {
    let correctChars = 0;
    let incorrectChars = 0;
    let extraChars = 0;
    let missedChars = 0;

    history.forEach((word, index) => {
      const target = words[index];
      const maxLength = Math.max(word.length, target.length);
      for (let i = 0; i < maxLength; i++) {
        if (i < target.length && i < word.length) {
          if (word[i] === target[i]) correctChars++;
          else incorrectChars++;
        } else if (i >= target.length) {
          extraChars++;
        } else if (i >= word.length) {
          missedChars++;
        }
      }
    });

    // Include currently typed word
    const currentTarget = words[history.length] || '';
    const currentLength = Math.max(typedInput.length, currentTarget.length);
    for (let i = 0; i < currentLength; i++) {
      if (i < currentTarget.length && i < typedInput.length) {
        if (typedInput[i] === currentTarget[i]) correctChars++;
        else incorrectChars++;
      } else if (i >= currentTarget.length && i < typedInput.length) {
        extraChars++;
      }
    }

    const timeElapsed = startTime ? (Date.now() - startTime) / 1000 : 1;
    const timeInMinutes = timeElapsed / 60;
    
    const grossWpm = (correctChars + incorrectChars + extraChars) / 5 / timeInMinutes;
    const netWpm = correctChars / 5 / timeInMinutes;
    const totalKeystrokes = correctChars + incorrectChars + extraChars + missedChars;
    const accuracy = totalKeystrokes > 0 ? (correctChars / totalKeystrokes) * 100 : 0;

    return {
      wpm: Math.round(Math.max(0, netWpm)),
      raw: Math.round(grossWpm),
      accuracy: Math.round(accuracy),
      correctChars,
      incorrectChars,
      extraChars,
      missedChars
    };
  };

  const recordChartData = () => {
    const metrics = calculateCurrentMetrics();
    const second = startTime ? Math.floor((Date.now() - startTime) / 1000) : 1;
    
    setChartData(prev => {
      // Avoid duplicate second entries
      if (prev.length > 0 && prev[prev.length - 1].second === second) return prev;
      return [...prev, {
        second,
        wpm: metrics.wpm,
        raw: metrics.raw,
        errors: metrics.incorrectChars + metrics.extraChars + metrics.missedChars - 
                (prev.length > 0 ? prev[prev.length - 1].totalErrorsAcc || 0 : 0),
        totalErrorsAcc: metrics.incorrectChars + metrics.extraChars + metrics.missedChars
      }];
    });
  };

  const calculateFinalStats = async () => {
    const metrics = calculateCurrentMetrics();
    setStats(metrics);
    recordChartData();
    
    if (useAuthStore.getState().isAuthenticated) {
      try {
        const timeElapsed = startTime ? (Date.now() - startTime) / 1000 : 1;
        await api.post('/tests/submit/', {
          mode: mode,
          duration: Math.round(timeElapsed) || 1,
          language: 'en',
          wpm: metrics.wpm,
          raw_wpm: metrics.raw,
          accuracy: metrics.accuracy,
          consistency: 90.0,
          characters_typed: metrics.correctChars + metrics.incorrectChars + metrics.extraChars + metrics.missedChars,
          correct_chars: metrics.correctChars,
          incorrect_chars: metrics.incorrectChars,
          extra_chars: metrics.extraChars,
          missed_chars: metrics.missedChars,
          wpm_history: []
        });
      } catch (err) {
        console.error('Failed to submit test result', err);
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (status === 'finished') return;
    
    if (status === 'idle' && e.key.length === 1) {
      setStatus('running');
      setStartTime(Date.now());
    }

    if (e.key === ' ') {
      e.preventDefault();
      if (typedInput.length > 0) {
        setHistory((prev) => [...prev, typedInput]);
        setTypedInput('');
        
        // Load more words if in time mode and getting close to end
        if (mode === 'time' && history.length + 5 >= words.length) {
          setWords((prev) => [...prev, ...generateWords(20, { punctuation: usePunctuation, numbers: useNumbers })]);
        }

        // Finish if in words mode and reached target, or quote mode reached end
        if ((mode === 'words' && history.length + 1 >= modeValue) || (mode === 'quote' && history.length + 1 >= words.length)) {
          finishTest();
        }
      }
    } else if (e.key === 'Backspace') {
      if (e.ctrlKey) {
        setTypedInput('');
      } else if (typedInput.length === 0 && history.length > 0) {
        const prevWord = history[history.length - 1];
        const targetWord = words[history.length - 1];
        if (prevWord !== targetWord) {
          setTypedInput(prevWord);
          setHistory((prev) => prev.slice(0, -1));
        }
      }
    }
  };

  const currentWordIndex = history.length;

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-[var(--bg-color)] border border-[var(--sub-color)]/20 p-3 rounded-lg shadow-xl text-sm font-mono flex flex-col gap-1">
          <p className="text-[var(--sub-color)] mb-1">Time: {label}s</p>
          {payload.map((p: any, i: number) => (
            <p key={i} style={{ color: p.color }} className="font-semibold">
              {p.name}: {p.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full max-w-[1250px] mx-auto flex flex-col items-center min-h-[400px]">
      
      {/* Configuration Bar (Monkeytype style 3 pills) */}
      <AnimatePresence>
        {status === 'idle' && (
          <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, height: 0, overflow: 'hidden' }}
            className="flex items-center gap-6 mb-12 text-xs font-medium text-[var(--sub-color)] transition-colors"
          >
            {/* Box 1: Punctuation & Numbers */}
            <div className="flex items-center gap-4 bg-[var(--sub-color)]/10 px-4 py-2.5 rounded-xl">
              <button 
                onClick={() => setUsePunctuation(!usePunctuation)}
                className={`flex items-center gap-1.5 hover:text-[var(--text-color)] transition-colors ${usePunctuation ? 'text-[var(--main-color)]' : ''}`}
                title="Punctuation"
              >
                @ punctuation
              </button>
              <button 
                onClick={() => setUseNumbers(!useNumbers)}
                className={`flex items-center gap-1.5 hover:text-[var(--text-color)] transition-colors ${useNumbers ? 'text-[var(--main-color)]' : ''}`}
                title="Numbers"
              >
                # numbers
              </button>
            </div>
            
            {/* Box 2: Modes */}
            <div className="flex items-center gap-4 bg-[var(--sub-color)]/10 px-4 py-2.5 rounded-xl">
              <button 
                onClick={() => setMode('time')}
                className={`flex items-center gap-2 hover:text-[var(--text-color)] transition-colors ${mode === 'time' ? 'text-[var(--main-color)]' : ''}`}
              >
                <Clock className="w-3.5 h-3.5" /> time
              </button>
              <button 
                onClick={() => setMode('words')}
                className={`flex items-center gap-2 hover:text-[var(--text-color)] transition-colors ${mode === 'words' ? 'text-[var(--main-color)]' : ''}`}
              >
                <Type className="w-3.5 h-3.5" /> words
              </button>
              <button 
                onClick={() => setMode('quote')}
                className={`flex items-center gap-2 hover:text-[var(--text-color)] transition-colors ${mode === 'quote' ? 'text-[var(--main-color)]' : ''}`}
              >
                <Quote className="w-3.5 h-3.5 fill-current" /> quote
              </button>
              <button className="flex items-center gap-2 hover:text-[var(--text-color)] transition-colors">
                <Mountain className="w-3.5 h-3.5" /> zen
              </button>
              <button className="flex items-center gap-2 hover:text-[var(--text-color)] transition-colors">
                <Wrench className="w-3.5 h-3.5" /> custom
              </button>
            </div>

            {/* Box 3: Values */}
            <div className="flex items-center gap-4 bg-[var(--sub-color)]/10 px-4 py-2.5 rounded-xl">
              {mode === 'time' && (
                [15, 30, 60, 120].map(val => (
                  <button 
                    key={val}
                    onClick={() => setModeValue(val)}
                    className={`hover:text-[var(--text-color)] transition-colors ${modeValue === val ? 'text-[var(--main-color)]' : ''}`}
                  >
                    {val}
                  </button>
                ))
              )}
              {mode === 'words' && (
                [10, 25, 50, 100].map(val => (
                  <button 
                    key={val}
                    onClick={() => setModeValue(val)}
                    className={`hover:text-[var(--text-color)] transition-colors ${modeValue === val ? 'text-[var(--main-color)]' : ''}`}
                  >
                    {val}
                  </button>
                ))
              )}
              {mode === 'quote' && (
                <span className="text-[var(--main-color)]">random quote</span>
              )}
              <button className="hover:text-[var(--text-color)] transition-colors border-l border-[var(--sub-color)]/20 pl-4 ml-2">
                <Wrench className="w-3.5 h-3.5" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Hidden Input */}
      <input
        ref={inputRef}
        type="text"
        className="opacity-0 absolute -z-10"
        value={typedInput}
        onChange={(e) => setTypedInput(e.target.value.trim())}
        onKeyDown={handleKeyDown}
        autoFocus
        spellCheck={false}
        autoComplete="off"
        autoCapitalize="off"
      />

      <AnimatePresence mode="wait">
        {status === 'finished' ? (
          /* Results Screen (Monkeytype Style) */
          <motion.div 
            key="results"
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex flex-col w-full gap-8"
          >
            <div className="flex flex-col md:flex-row gap-8 w-full">
              {/* Left Column Stats */}
              <div className="flex flex-col gap-6 md:w-48 shrink-0">
                <div>
                  <p className="text-[var(--sub-color)] text-xl mb-1 font-mono">wpm</p>
                  <p className="text-7xl font-black text-[var(--main-color)] font-mono leading-none">{stats.wpm}</p>
                </div>
                <div>
                  <p className="text-[var(--sub-color)] text-xl mb-1 font-mono">acc</p>
                  <p className="text-5xl font-black text-[var(--text-color)] font-mono leading-none">{stats.accuracy}%</p>
                </div>
                <div className="mt-auto pt-8">
                  <p className="text-[var(--sub-color)] text-sm font-mono">test type</p>
                  <p className="text-[var(--main-color)] text-sm font-mono">{mode} {modeValue}</p>
                  <p className="text-[var(--sub-color)] text-sm font-mono">english</p>
                </div>
              </div>

              {/* Chart */}
              <div className="flex-1 h-[300px] w-full min-w-0">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--sub-color)" opacity={0.2} vertical={false} />
                    <XAxis 
                      dataKey="second" 
                      stroke="var(--sub-color)" 
                      tick={{ fill: 'var(--sub-color)', fontSize: 12 }} 
                      tickLine={false} 
                      axisLine={false} 
                    />
                    <YAxis 
                      yAxisId="left" 
                      stroke="var(--sub-color)" 
                      tick={{ fill: 'var(--sub-color)', fontSize: 12 }} 
                      tickLine={false} 
                      axisLine={false}
                    />
                    <YAxis 
                      yAxisId="right" 
                      orientation="right" 
                      stroke="var(--sub-color)" 
                      tick={{ fill: 'var(--sub-color)', fontSize: 12 }} 
                      tickLine={false} 
                      axisLine={false} 
                      domain={[0, 'dataMax + 2']}
                    />
                    <RechartsTooltip content={<CustomTooltip />} />
                    
                    {/* WPM Line */}
                    <Line 
                      yAxisId="left"
                      type="monotone" 
                      dataKey="wpm" 
                      name="WPM"
                      stroke="var(--main-color)" 
                      strokeWidth={3} 
                      dot={false}
                      activeDot={{ r: 6, fill: 'var(--bg-color)', stroke: 'var(--main-color)', strokeWidth: 2 }}
                    />
                    
                    {/* Raw WPM Line */}
                    <Line 
                      yAxisId="left"
                      type="monotone" 
                      dataKey="raw" 
                      name="Raw"
                      stroke="var(--sub-color)" 
                      strokeWidth={2} 
                      strokeDasharray="5 5"
                      dot={false}
                      activeDot={false}
                    />

                    {/* Errors Scatter/Line */}
                    <Line 
                      yAxisId="right"
                      type="step" 
                      dataKey="errors" 
                      name="Errors"
                      stroke="transparent" 
                      dot={{ r: 3, fill: 'var(--error-color)', strokeWidth: 0 }}
                      activeDot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Bottom Row Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full mt-4">
              <div>
                <p className="text-[var(--sub-color)] text-sm font-mono mb-1">raw</p>
                <p className="text-3xl text-[var(--text-color)] font-mono">{stats.raw}</p>
              </div>
              <div>
                <p className="text-[var(--sub-color)] text-sm font-mono mb-1">characters</p>
                <p className="text-2xl text-[var(--text-color)] font-mono tracking-tight">
                  {stats.correctChars}/<span className="text-[var(--error-color)] opacity-80">{stats.incorrectChars}</span>/<span className="text-[var(--error-extra-color)] opacity-80">{stats.extraChars}</span>/<span className="text-[var(--sub-color)] opacity-80">{stats.missedChars}</span>
                </p>
              </div>
              <div>
                <p className="text-[var(--sub-color)] text-sm font-mono mb-1">consistency</p>
                <p className="text-3xl text-[var(--text-color)] font-mono">
                  {/* Mock consistency for now */}
                  {Math.max(0, 100 - (stats.incorrectChars * 2))}%
                </p>
              </div>
              <div>
                <p className="text-[var(--sub-color)] text-sm font-mono mb-1">time</p>
                <p className="text-3xl text-[var(--main-color)] font-mono">
                  {chartData.length > 0 ? chartData[chartData.length - 1].second : 0}s
                </p>
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center justify-center gap-6 mt-12 text-[var(--sub-color)]">
              <button 
                onClick={resetTest}
                className="p-3 hover:text-[var(--text-color)] transition-colors focus:outline-none"
                title="Next Test"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
              <button 
                onClick={resetTest}
                className="p-3 hover:text-[var(--text-color)] transition-colors focus:outline-none"
                title="Restart Test"
              >
                <RotateCcw className="w-5 h-5" />
              </button>
              <button 
                className="p-3 hover:text-[var(--error-color)] transition-colors focus:outline-none"
                title="Report Issue"
              >
                <ShieldAlert className="w-5 h-5" />
              </button>
            </div>
          </motion.div>
        ) : (
          /* Typing Canvas */
          <motion.div 
            key="typing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="w-full relative mt-8"
          >
            {/* Header: Language & Time / Progress */}
            <div className="relative flex justify-center items-end mb-4 text-[var(--sub-color)] font-mono h-8 w-full max-w-full">
              <div className="absolute left-0 bottom-1 flex items-center gap-4 transition-opacity text-[var(--main-color)] text-2xl">
                {(status === 'running' || status === 'idle') && (
                  <span>{mode === 'time' ? (status === 'idle' ? modeValue : timeLeft) : `${history.length}/${modeValue}`}</span>
                )}
              </div>
              <div className="flex items-center gap-2 hover:text-[var(--text-color)] transition-colors cursor-pointer text-xs mb-1">
                <Globe className="w-3.5 h-3.5" /> english
              </div>
            </div>

            {/* Typing Container */}
            <div 
              className="relative text-[28px] font-mono leading-[1.5em] overflow-hidden select-none h-[126px]"
              style={{ color: 'var(--sub-color)' }}
            >
              <div 
                ref={wordsContainerRef}
                className="flex flex-wrap gap-x-[0.4em] w-full content-start transition-transform duration-200 ease-out"
                style={{
                  transform: `translateY(-${scrollOffset}px)`
                }}
              >
                {words.map((word, wordIdx) => {
                  const isActive = wordIdx === currentWordIndex;
                  const isHistory = wordIdx < currentWordIndex;
                  
                  let historyWord = '';
                  if (isHistory) historyWord = history[wordIdx];
                  if (isActive) historyWord = typedInput;

                  const isWordWrong = isHistory && historyWord !== word;
                  
                  return (
                    <div 
                      key={wordIdx} 
                      className={`relative flex ${isWordWrong ? 'border-b-2 border-[var(--error-color)]' : ''}`}
                    >
                      {/* Letters */}
                      {word.split('').map((char, charIdx) => {
                        let colorClass = '';
                        let isCaretHere = false;
                        
                        if (isHistory) {
                          colorClass = historyWord[charIdx] === char 
                            ? 'text-[var(--text-color)]' 
                            : 'text-[var(--error-color)]';
                        } else if (isActive) {
                          if (charIdx < typedInput.length) {
                            colorClass = typedInput[charIdx] === char 
                              ? 'text-[var(--text-color)]' 
                              : 'text-[var(--error-color)] bg-[var(--error-color)]/20 rounded-sm';
                          }
                          isCaretHere = charIdx === typedInput.length;
                        }

                        return (
                          <span key={charIdx} className={`relative ${colorClass}`}>
                            {isCaretHere && (
                              <motion.div
                                className="absolute left-0 top-0 bottom-0 w-[2px] bg-[var(--caret-color)] z-10"
                                initial={{ opacity: 1 }}
                                animate={{ opacity: [1, 0, 1] }}
                                transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                              />
                            )}
                            {char}
                          </span>
                        );
                      })}
                      
                      {/* Extra typed characters */}
                      {(isHistory || isActive) && historyWord.length > word.length && (
                        <div className="flex text-[var(--error-extra-color)] opacity-70">
                          {historyWord.slice(word.length).split('').map((char, i) => {
                            const isCaretHere = isActive && i + word.length === typedInput.length;
                            return (
                              <span key={i} className="relative">
                                {isCaretHere && (
                                  <motion.div
                                    className="absolute left-0 top-0 bottom-0 w-[2px] bg-[var(--caret-color)] z-10"
                                    initial={{ opacity: 1 }}
                                    animate={{ opacity: [1, 0, 1] }}
                                    transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                                  />
                                )}
                                {char}
                              </span>
                            );
                          })}
                        </div>
                      )}
                      
                      {/* Space caret fallback (at end of active word) */}
                      {isActive && typedInput.length === word.length && (
                        <span className="relative">
                           <motion.div
                             className="absolute left-0 top-0 bottom-0 w-[2px] bg-[var(--caret-color)] z-10"
                             initial={{ opacity: 1 }}
                             animate={{ opacity: [1, 0, 1] }}
                             transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                           />
                        </span>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Restart Button & Keyboard Shortcuts */}
            <div className="flex flex-col items-center mt-12 opacity-70 hover:opacity-100 transition-opacity">
              <button 
                onClick={resetTest}
                className="p-3 mb-2 text-[var(--sub-color)] hover:bg-[var(--sub-color)]/10 hover:text-[var(--text-color)] rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--main-color)]"
                title="Restart Test (Tab + Enter)"
              >
                <RotateCcw className="w-5 h-5" />
              </button>
              
              {status === 'idle' && (
                <div className="flex flex-col items-center gap-1 text-[var(--sub-color)]/70 text-xs font-mono">
                  <p>
                    <kbd className="bg-[var(--sub-color)]/10 px-2 py-0.5 rounded mr-1">tab</kbd> + 
                    <kbd className="bg-[var(--sub-color)]/10 px-2 py-0.5 rounded mx-1">enter</kbd> - restart test
                  </p>
                  <p>
                    <kbd className="bg-[var(--sub-color)]/10 px-2 py-0.5 rounded mx-1">esc</kbd> or 
                    <kbd className="bg-[var(--sub-color)]/10 px-2 py-0.5 rounded mx-1">ctrl</kbd> + 
                    <kbd className="bg-[var(--sub-color)]/10 px-2 py-0.5 rounded mx-1">shift</kbd> + 
                    <kbd className="bg-[var(--sub-color)]/10 px-2 py-0.5 rounded mx-1">p</kbd> - command line
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
