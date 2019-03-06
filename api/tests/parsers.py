from django.test import TestCase
from api.parsers import HackerNewsHtmlParser, NewsPair


class HackerNewsHtmlParserTestCase(TestCase):
    def test_pairs(self):
        parser = HackerNewsHtmlParser()
        parser.feed("""\
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
        </table>""")
        self.assertEqual(parser.pairs, [NewsPair('url1', 'title1'), NewsPair('url2', 'title2')])

    def test_pairs_fails(self):
        cases = {
            "Table class not checked": """
                <table class="table_class">
                    <tr class="athing">
                        <td class="title">
                            <a href="url1" class="storylink">
                                title1
                            </a>
                        </td>
                    </tr>
                </table>""",
            "Row class not checked": """
                <table class="itemlist">
                    <tr class="other_row_class">
                        <td class="title">
                            <a href="url1" class="storylink">
                                title1
                            </a>
                        </td>
                    </tr>
                </table>""",
            "Cell class not checked": """
                <table class="itemlist">
                    <tr class="athing">
                        <td class="cell_class">
                            <a href="url1" class="storylink">
                                title1
                            </a>
                        </td>
                    </tr>
                </table>""",
            "Link class not checked": """
                <table class="itemlist">
                    <tr class="athing">
                        <td class="title">
                            <a href="url1" class="link_class">
                                title1
                            </a>
                        </td>
                    </tr>
                </table>""",

            # tags
            "Table tag not checked": """
                <ul class="itemlist">
                    <tr class="athing">
                        <td class="title">
                            <a href="url1" class="storylink">
                                title1
                            </a>
                        </td>
                    </tr>
                </ul>""",
            "Row tag not checked": """
                <table class="itemlist">
                    <li class="athing">
                        <td class="title">
                            <a href="url1" class="storylink">
                                title1
                            </a>
                        </td>
                    </li>
                </table>""",
            "Cell tag not checked": """
                <table class="itemlist">
                    <tr class="athing">
                        <span class="title">
                            <a href="url1" class="storylink">
                                title1
                            </a>
                        </span>
                    </tr>
                </table>""",
            "Link tag not checked": """
                <table class="itemlist">
                    <tr class="athing">
                        <td class="title">
                            <div href="url1" class="storylink">
                                title1
                            </div>
                        </td>
                    </tr>
                </table>""",
        }
        for msg, case in cases.items():
            parser = HackerNewsHtmlParser()
            parser.feed(case)
            self.assertEqual([], parser.pairs, msg)
