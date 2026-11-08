import unittest

from lxml import etree

from convert import Page, Renderer


class VariableListTests(unittest.TestCase):
    def render(self, description):
        source = etree.fromstring(f"""<variablelist>
          <varlistentry><term>Signature</term><listitem><para>Header.</para></listitem></varlistentry>
          <varlistentry><term>Flags</term><listitem><para>{description}</para></listitem></varlistentry>
        </variablelist>""")
        renderer = Renderer("en", {}, Page("ref", "copy", "reference", "copy", 1))
        return renderer.tag_variablelist(source, 2)

    def test_inline_description_remains_a_table(self):
        self.assertIn("| Flags | A `flag`. |", self.render("A <literal>flag</literal>."))

    def test_nested_list_preserves_blocks_and_text(self):
        output = self.render("""Before.<variablelist><varlistentry>
          <term>Bit 16</term><listitem><para>Contains OIDs.</para></listitem>
        </varlistentry></variablelist>After.""")
        self.assertTrue(output.startswith("{{< fields >}}"))
        self.assertIn('{{< field name="Bit 16" >}}', output)
        for text in ("Before.", "Contains OIDs.", "After."):
            self.assertIn(text, output)
        self.assertNotIn("<br>{{<", output)
        self.assertFalse(any(line.startswith("|") for line in output.splitlines()))


if __name__ == "__main__":
    unittest.main()
