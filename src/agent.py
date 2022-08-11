import os
import platform
import sys
import time

import build_config
from plex.log import Log
from service.caribbeancom import searcher as caribbeancom_searcher
from service.caribbeancom import updater as caribbeancom_updater
from service.caribbeancom_pr import searcher as caribbeancom_pr_searcher
from service.caribbeancom_pr import updater as caribbeancom_pr_updater
from service.fanza import searcher as fanza_searcher
from service.fanza import updater as fanza_updater
from service.heyzo import searcher as heyzo_searcher
from service.heyzo import updater as heyzo_updater
from service.ichi_pondo import searcher as ichi_pondo_searcher
from service.ichi_pondo import updater as ichi_pondo_updater
from service.knights_visual import searcher as knights_visual_searcher
from service.knights_visual import updater as knights_visual_updater
from service.s_cute import searcher as s_cute_searcher
from service.s_cute import updater as s_cute_updater
from utility import file_helper
from utility import image_helper
from utility import mixpanel_helper
from utility import sentry_helper
from utility import user_helper


# noinspection PyMethodMayBeStatic,DuplicatedCode
class JavMovieAgent:

    def __init__(self, name):
        start_time_in_seconds = time.time()
        Log.Info("Initializing agent")
        Log.Debug("name: {}".format(name))
        Log.Debug('plex_version: {}'.format(build_config.plex_version))
        Log.Debug("version: {}".format(build_config.version))
        Log.Debug("git_hash: {}".format(build_config.git_hash))
        Log.Debug("build_number: {}".format(build_config.build_number))
        Log.Debug("build_datetime: {}".format(build_config.build_datetime))
        Log.Debug("environment: {}".format(build_config.environment))
        Log.Debug("sys.version: {}".format(sys.version.replace("\n", "")))
        Log.Debug("sys.version_info: {}".format(sys.version_info))
        Log.Debug("sys.platform: {}".format(sys.platform))
        Log.Debug("sys.executable: {}".format(sys.executable))
        Log.Debug("platform.system: {}".format(platform.system().lower()))
        Log.Debug("platform.mac_ver: {}".format(platform.mac_ver()))
        Log.Debug("platform.linux_distribution: {}".format(platform.linux_distribution()))
        Log.Debug("platform.win32_ver: {}".format(platform.win32_ver()))
        for i, path in enumerate(sys.path): Log.Debug("sys.path[{}]: {}".format(i, path))  # noqa

        # init user id
        user_id = user_helper.get_user_id()
        Log.Debug('user_id: {}'.format(user_id))

        # init mixpanel, sentry and then agent
        mixpanel_helper.initialize(user_id)
        if user_helper.is_new_user_id: mixpanel_helper.track.installed()  # noqa
        sentry_helper.init_sentry(user_id)

        # done
        time_spent_in_seconds = time.time() - start_time_in_seconds
        image_rocessing_capability = image_helper.can_analyze_images
        mixpanel_helper.track.initialized(image_rocessing_capability, time_spent_in_seconds)

    def search(self, results, media, lang, manual, primary):
        """
        This is called when you click on "fix match" button in Plex.
        :type results: ObjectContainer
        :type media: Media
        :type lang: str
        :type manual: bool
        :return:
        """
        start_time_in_seconds = time.time()
        Log.Info("Searching media")
        Log.Debug("results: {}".format(results))
        Log.Debug("media: {}".format(media))
        Log.Debug("lang: {}".format(lang))
        Log.Debug("manual: {}".format(manual))
        Log.Debug("primary: {}".format(primary))
        Log.Debug("media.id: {}".format(media.id))
        Log.Debug("media.name: {}".format(media.name))
        Log.Debug("media.year: {}".format(media.year))
        Log.Debug("media.filename: {}".format(media.items[0].parts[0].file))

        # generating keywords from directory and filename
        filename = media.items[0].parts[0].file
        directory = os.path.basename(os.path.dirname(filename))
        product_id, part_number = file_helper.extract_product_id_and_part_number(filename)
        Log.Debug("directory: {}".format(directory))
        Log.Debug("product_id: {}".format(product_id))
        Log.Debug("part_number: {}".format(part_number))

        # detect if there are extra info like "1PON-121015_001 (121015_3314)"
        # TODO: do something with this info
        partitioned_product_id = product_id.partition(' ')
        if len(partitioned_product_id) > 2:
            product_id = partitioned_product_id[0]
            Log.Debug("it seems like there are more info after production id: {}".format(partitioned_product_id[2]))
            Log.Debug("it is ignored for now, so it became: {}".format(product_id))

        # query fanza api with keywords
        caribbeancom_searcher.search(results, part_number, directory)
        caribbeancom_searcher.search(results, part_number, product_id)
        caribbeancom_pr_searcher.search(results, part_number, directory)
        caribbeancom_pr_searcher.search(results, part_number, product_id)
        fanza_searcher.search(results, part_number, directory)
        fanza_searcher.search(results, part_number, product_id)
        knights_visual_searcher.search(results, part_number, directory)
        knights_visual_searcher.search(results, part_number, product_id)
        heyzo_searcher.search(results, part_number, directory)
        heyzo_searcher.search(results, part_number, product_id)
        ichi_pondo_searcher.search(results, part_number, directory)
        ichi_pondo_searcher.search(results, part_number, product_id)
        s_cute_searcher.search(results, part_number, directory)
        s_cute_searcher.search(results, part_number, product_id)

        # done
        Log.Info("Search is done")
        time_spent_in_seconds = time.time() - start_time_in_seconds
        mixpanel_helper.track.searched(media, lang, manual, primary, filename, directory, product_id, part_number, results, time_spent_in_seconds)

    def update(self, metadata, media, lang, force, child_guid, child_id, periodic, prefs):
        """
        :type metadata: Movie
        :type media: Media
        :type lang: str
        :type force: bool
        """
        start_time_in_seconds = time.time()
        Log.Info("Updating media")
        Log.Debug("metadata: {}".format(metadata))
        Log.Debug("metadata.id: {}".format(metadata.id))
        Log.Debug("metadata.title: {}".format(metadata.title))
        Log.Debug("metadata.year: {}".format(metadata.year))
        Log.Debug("media: {}".format(media))
        Log.Debug("lang: {}".format(lang))
        Log.Debug("force: {}".format(force))
        Log.Debug("child_guid: {}".format(child_guid))
        Log.Debug("child_id: {}".format(child_id))
        Log.Debug("periodic: {}".format(periodic))
        Log.Debug("prefs: {}".format(prefs))

        # actual updating
        caribbeancom_updater.update(metadata)
        caribbeancom_pr_updater.update(metadata)
        fanza_updater.update(metadata)
        knights_visual_updater.update(metadata)
        heyzo_updater.update(metadata)
        ichi_pondo_updater.update(metadata)
        s_cute_updater.update(metadata)

        # done
        Log.Info("Update is done")
        time_spent_in_seconds = time.time() - start_time_in_seconds
        mixpanel_helper.track.updated(metadata, lang, force, child_guid, child_id, periodic, prefs, time_spent_in_seconds)
