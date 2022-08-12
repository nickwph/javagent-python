import time
from difflib import SequenceMatcher

import api
from plex.agent import MetadataSearchResult
from plex.locale import Locale
from plex.log import Log
from utility import mixpanel_helper


def search(results, part_number, keyword):
    """
    :type results: ObjectContainer[MetadataSearchResult]
    :type part_number: Optional[int]
    :type keyword: str
    """
    if not keyword.startswith("KV") or not keyword.startswith("KV-"):
        return

    product_id = keyword
    if keyword.startswith("KV") and not keyword.startswith("KV-"):
        product_id = product_id.replace("KV", "KV-")

    Log.Info("Search item with keyword: {}".format(product_id))
    items = api.search(product_id)

    for item in items:
        start_time_in_seconds = time.time()
        metadata_id = "knights-visual-" + item.id + ("@{}".format(part_number) if part_number is not None else "")
        score = int(SequenceMatcher(None, keyword, item.id).ratio() * 150)
        result = MetadataSearchResult(
            id=metadata_id,
            name=u"{} {}".format(item.id, item.title),
            year=item.upload_year,
            lang=Locale.Language.Japanese,
            thumb=item.thumbnail_url,
            score=score)
        results.Append(result)
        Log.Info(u"Added search result: {}".format(result))
        time_spent_in_seconds = time.time() - start_time_in_seconds
        mixpanel_helper.track.search.result_returned('knights-visual', result, time_spent_in_seconds)
