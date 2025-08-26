from datetime import datetime, timedelta
from collections import Counter
from typing import Iterable


ISO_FMT = "%Y-%m-%d"




def to_local_date(dt_txt: str, tz_offset: int) -> str:
	# OpenWeather returns UTC-like dt_txt (no tz info). tz_offset is seconds.
	dt = datetime.fromisoformat(dt_txt)
	local = dt + timedelta(seconds=tz_offset)
	return local.strftime(ISO_FMT)




def mode_text(texts: Iterable[str]) -> str:
	c = Counter(t.lower() for t in texts)
	return c.most_common(1)[0][0] if c else ""