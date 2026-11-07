import React from 'react';

// Stand-in for an asset that hasn't been made yet. Visible only in debug (preview) renders;
// a final render with missing assets shows a faint outline so nothing looks broken by accident.
export const Placeholder: React.FC<{ label: string; style: React.CSSProperties; debug: boolean }> = ({ label, style, debug }) => (
  <div
    style={{
      position: 'absolute',
      border: debug ? '4px dashed rgba(255,255,255,0.85)' : '2px solid rgba(255,255,255,0.15)',
      borderRadius: 18,
      background: debug ? 'rgba(30,20,32,0.35)' : 'transparent',
      color: '#fff',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      textAlign: 'center',
      font: '600 30px sans-serif',
      padding: 10,
      boxSizing: 'border-box',
      ...style,
    }}
  >
    {debug ? label : null}
  </div>
);
