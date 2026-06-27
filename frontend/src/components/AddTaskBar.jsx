import React, { useState, useRef, useEffect } from 'react';
import api from '../services/api';
import './AddTaskBar.css';

function AddTaskBar({ defaultDate, channels, onTaskAdded }) {
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState('');
  
  // Selections
  const [plannedDate, setPlannedDate] = useState(defaultDate);
  const [priority, setPriority] = useState('none'); // urgent, high, medium, low, none
  const [channelId, setChannelId] = useState(channels.length > 0 ? channels[0].id : null);
  
  // Sync channelId when channels are loaded asynchronously
  useEffect(() => {
    if (!channelId && channels.length > 0) {
      setChannelId(channels[0].id);
    }
  }, [channels, channelId]);
  
  // Popovers
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [showPriorityPicker, setShowPriorityPicker] = useState(false);
  const [showChannelPicker, setShowChannelPicker] = useState(false);
  const [channelSearch, setChannelSearch] = useState('');

  const containerRef = useRef(null);

  // Close on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
        setShowDatePicker(false);
        setShowPriorityPicker(false);
        setShowChannelPicker(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSubmit = async () => {
    if (!title.trim()) return;
    try {
      await api.post('/api/tasks', {
        title: title.trim(),
        planned_date: plannedDate,
        priority,
        channel_id: channelId
      });
      setTitle('');
      setIsOpen(false);
      if (onTaskAdded) onTaskAdded();
    } catch (err) {
      console.error("Failed to add task", err);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSubmit();
    }
  };

  const todayStr = new Date().toISOString().split('T')[0];

  const getPriorityIcon = (prio) => {
    switch(prio) {
      case 'urgent': return '❗';
      case 'high': return '🔴';
      case 'medium': return '🟡';
      case 'low': return '🔵';
      default: return '⚪';
    }
  };

  const getPriorityLabel = (prio) => {
    if (prio === 'none') return 'No priority';
    return prio.charAt(0).toUpperCase() + prio.slice(1);
  };

  const getChannelName = (id) => {
    const c = channels.find(x => x.id === parseInt(id));
    return c ? c.name : 'Unassigned';
  };

  if (!isOpen) {
    return (
      <button className="add-task-trigger" onClick={() => setIsOpen(true)}>
        + Add task
      </button>
    );
  }

  return (
    <div className="add-task-bar active" ref={containerRef}>
      <input 
        autoFocus
        type="text" 
        className="add-task-input" 
        placeholder="Task name" 
        value={title}
        onChange={e => setTitle(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      
      <div className="add-task-toolbar">
        <div></div> {/* Left spacer instead of tip */}
        
        <div className="toolbar-actions">
          {/* Add Button */}
          <button className="btn btn-primary" style={{ padding: '4px 12px', fontSize: '12px' }} onClick={handleSubmit}>Add</button>
          {/* Date Picker */}
          <div className="toolbar-item">
            <button onClick={() => {setShowDatePicker(!showDatePicker); setShowPriorityPicker(false); setShowChannelPicker(false);}}>
              📅 {plannedDate === todayStr ? 'Today' : plannedDate || 'Someday'}
            </button>
            {showDatePicker && (
              <div className="popover date-popover">
                <div className="popover-shortcuts">
                  <div onClick={() => {setPlannedDate(todayStr); setShowDatePicker(false);}}>📅 Today</div>
                  <div onClick={() => {
                    const d = new Date(); d.setDate(d.getDate() + 7);
                    setPlannedDate(d.toISOString().split('T')[0]); setShowDatePicker(false);
                  }}>📆 In the next week</div>
                  <div onClick={() => {setPlannedDate(null); setShowDatePicker(false);}}>⏳ Someday</div>
                </div>
                <div className="popover-divider"></div>
                <div className="popover-calendar">
                  <label>Schedule exact date</label>
                  <input 
                    type="date" 
                    min={todayStr}
                    value={plannedDate || ''}
                    onChange={(e) => {
                      setPlannedDate(e.target.value);
                      setShowDatePicker(false);
                    }}
                  />
                </div>
              </div>
            )}
          </div>

          {/* Channel Picker with create option */}
          <div className="toolbar-item">
            <button onClick={() => {setShowChannelPicker(!showChannelPicker); setShowPriorityPicker(false); setShowDatePicker(false);}}>
              # {channelId ? getChannelName(channelId) : 'Unassigned'}
            </button>
            {showChannelPicker && (
              <div className="popover channel-popover" style={{ padding: '8px', minWidth: '180px' }}>
                <div style={{ fontSize: '11px', color: '#888', marginBottom: '8px' }}>Assign to channel:</div>
                <input 
                  type="text" 
                  autoFocus
                  placeholder="Search..." 
                  value={channelSearch}
                  onChange={e => setChannelSearch(e.target.value)}
                  style={{ width: '100%', marginBottom: '8px', background: 'transparent', border: 'none', borderBottom: '1px solid #444', color: '#fff', outline: 'none' }}
                />
                <div className="popover-item" onClick={() => {setChannelId(null); setShowChannelPicker(false);}}>
                  # Unassigned {channelId === null && '✓'}
                </div>
                {channels.filter(c => c.name.toLowerCase().includes(channelSearch.toLowerCase())).map(c => (
                  <div key={c.id} className="popover-item" onClick={() => {setChannelId(c.id); setShowChannelPicker(false);}}>
                    <span style={{ color: c.color || '#10B981', marginRight: '4px' }}>#</span> {c.name} {channelId === c.id && '✓'}
                  </div>
                ))}
                {channelSearch && !channels.find(c => c.name.toLowerCase() === channelSearch.toLowerCase()) && (
                  <div className="popover-item" style={{ color: '#10B981' }} onClick={async () => {
                    try {
                      // Support sending data to our local backend directly to create a channel
                      const res = await api.post('/api/channels', { name: channelSearch.toLowerCase(), color: '#10B981' });
                      setChannelId(res.data?.id || res.id);
                      setShowChannelPicker(false);
                      setChannelSearch('');
                      if (onTaskAdded) onTaskAdded(); // refresh channels list from parent
                    } catch (e) {
                      console.error("Failed to create channel", e);
                    }
                  }}>
                    + Create "{channelSearch.toLowerCase()}"
                  </div>
                )}
                <div className="popover-divider"></div>
                <div className="popover-item" style={{ color: '#3b82f6', fontSize: '11px' }}>Manage channels</div>
              </div>
            )}
          </div>

          {/* Priority Picker */}
          <div className="toolbar-item">
            <button onClick={() => {setShowPriorityPicker(!showPriorityPicker); setShowDatePicker(false); setShowChannelPicker(false);}}>
              {getPriorityIcon(priority)}
            </button>
            {showPriorityPicker && (
              <div className="popover priority-popover">
                <div className="popover-header">Set priority</div>
                <div className="popover-item" onClick={() => {setPriority('urgent'); setShowPriorityPicker(false);}}>❗ Urgent</div>
                <div className="popover-item" onClick={() => {setPriority('high'); setShowPriorityPicker(false);}}>🔴 High</div>
                <div className="popover-item" onClick={() => {setPriority('medium'); setShowPriorityPicker(false);}}>🟡 Medium</div>
                <div className="popover-item" onClick={() => {setPriority('low'); setShowPriorityPicker(false);}}>🔵 Low</div>
                <div className="popover-item" onClick={() => {setPriority('none'); setShowPriorityPicker(false);}}>⚪ No priority {priority === 'none' && '✓'}</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AddTaskBar;
