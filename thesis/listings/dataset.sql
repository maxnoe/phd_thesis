SELECT
	fNight,
	fRunID,
  fThresholdMinSet,
	(TIMESTAMPDIFF(SECOND, fRunStart, fRunStop) * fEffectiveOn) AS ontime
FROM RunInfo
WHERE 
	fSourceKEY = 5
	AND fRunTypeKey = 1
	AND fNight BETWEEN 20131001 AND 20140205
	AND fZenithDistanceMax < 30
	AND fMoonZenithDistance > 100
	AND fCurrentsMedMeanBeg < 8
	AND fTriggerRateMedian > 40
	AND fTriggerRateMedian < 85
	AND fThresholdMinSet < 350
	AND fEffectiveOn > 0.95
;

