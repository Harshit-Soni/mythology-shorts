import React from 'react';
import { Composition } from 'remotion';
import { Episode, episodeDuration } from './Episode';
import { IllustratedEpisode, illustratedDuration } from './IllustratedEpisode';
import { EPISODES } from './generated/data';
import type { EpisodeProps, Lang } from './lib/types';

// One composition per episode per language, e.g. "S01E01-en", "S01E01-hi".
export const Root: React.FC = () => (
  <>
    {Object.entries(EPISODES).flatMap(([id, entry]) =>
      (['en', 'hi'] as Lang[]).map((lang) => (
        <Composition<any, EpisodeProps>
          key={`${id}-${lang}`}
          id={`${id}-${lang}`}
          component={Episode}
          fps={entry.spec.fps}
          width={entry.spec.width}
          height={entry.spec.height}
          durationInFrames={episodeDuration(id, lang, entry.spec.fps)}
          defaultProps={{ episodeId: id, lang, debug: true }}
        />
      )),
    )}
    {/* Illustrated version, when episodes/<ID>/illustrated/03-shots.json exists: "S01E01-illustrated-en" */}
    {Object.entries(EPISODES).filter(([, e]) => e.shots).flatMap(([id, entry]) =>
      (['en', 'hi'] as Lang[]).map((lang) => (
        <Composition<any, EpisodeProps>
          key={`${id}-illustrated-${lang}`}
          id={`${id}-illustrated-${lang}`}
          component={IllustratedEpisode}
          fps={entry.spec.fps}
          width={entry.spec.width}
          height={entry.spec.height}
          durationInFrames={illustratedDuration(id, lang, entry.spec.fps)}
          defaultProps={{ episodeId: id, lang, debug: true }}
        />
      )),
    )}
  </>
);
