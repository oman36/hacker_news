import datetime

from django.test import TestCase
from django.utils import timezone

from api.models import News
from api.services import HackerNewsSaver


class HackerNewsSaverTestCase(TestCase):
    @staticmethod
    def _get_content(flag: dict, content: str):
        flag['value'] = True
        return content

    def test_pairs(self):
        saver = HackerNewsSaver()
        flag = {'value': False}
        news_items = {
            'title0': News(title='title0', url='url0'),
            'title1': News(title='title1', url='url1'),
        }
        for item in news_items.values():
            item.save()
            item.created = timezone.now() - datetime.timedelta(days=30)
            item.save()

        setattr(saver, '_get_content', lambda *args: self._get_content(flag, """\
        <table class="itemlist">
            <tr class="athing">
                <td class="title">
                    <a href="url1" class="storylink">
                        title1
                    </a>
                </td>
            </tr>
            <tr class="athing">
                <td class="title">
                    <a href="url2" class="storylink">
                        title2
                    </a>
                </td>
            </tr>
        </table>"""))
        now = timezone.now()
        saver.save()
        self.assertTrue(flag['value'], 'Function _get_content was not called')
        now_exists = News.objects.all()
        self.assertLessEqual(len(now_exists), 3, 'Redundant news items were added')
        self.assertEqual(3, len(now_exists), 'News item was not added')
        for item in now_exists:
            if item.title in news_items:
                self.assertEqual(item.created, news_items[item.title].created,
                                 'created for existed row was updated')
            else:
                self.assertGreaterEqual(item.created, now, 'New item has invalid created time')
                self.assertEqual(item.title, 'title2', 'New item has invalid title')
                self.assertEqual(item.url, 'url2', 'New item has invalid url')

        setattr(saver, '_get_content', lambda *args: self._get_content(flag, ''))
        self.assertRaises(RuntimeError, saver.save)
