import React from 'react';
import { Composition } from 'remotion';
import { Episode, episodeDuration } from './Episode';
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
  </>
);
