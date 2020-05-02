import json
import re

from django.test import TransactionTestCase
from graphene_django.utils import GraphQLTestCase

from experiment_django3.insurances.tests import DummyMixin
from experiment_django3.insurances.utils import extract_params
from schema import schema


class TestUtil(TransactionTestCase):
    def test_string_extractor(self):
        input = b'{"query":"query{\\n  allPremiums(sumInsured: 10000, premium: 90){\\n    edges{\\n      node{\\n        percentage\\n      \\tsumInsured\\n        premium\\n      }\\n    }\\n  }\\n}\\n\\n\\n# Welcome to GraphiQL\\n#\\n# GraphiQL is an in-browser tool for writing, validating, and\\n# testing GraphQL queries.\\n#\\n# Type queries into this side of the screen, and you will see intelligent\\n# typeaheads aware of the current GraphQL type schema and live syntax and\\n# validation errors highlighted within the text.\\n#\\n# GraphQL queries typically start with a \\"{\\" character. Lines that starts\\n# with a # are ignored.\\n#\\n# An example GraphQL query might look like:\\n#\\n#     {\\n#       field(arg: \\"value\\") {\\n#         subField\\n#       }\\n#     }\\n#\\n# Keyboard shortcuts:\\n#\\n#  Prettify Query:  Shift-Ctrl-P (or press the prettify button above)\\n#\\n#     Merge Query:  Shift-Ctrl-M (or press the merge button above)\\n#\\n#       Run Query:  Ctrl-Enter (or press the play button above)\\n#\\n#   Auto Complete:  Ctrl-Space (or just start typing)\\n#\\n\\n# query{\\n#   allOccupations{\\n#     edges{\\n#     \\tnode{\\n#         name\\n#       }\\n#     }\\n#   }\\n# }\\n\\n","variables":null}'
        data = json.loads(input)
        # 'sumInsured: 10000, premium: 90'
        input = re.search('\(([^)]+)', data['query']).group(1)
        expected_result = {
            'sum_insured': 10000,
            'premium': 90,
        }
        ans = extract_params(input)
        self.assertDictEqual(expected_result, ans)


class TestGraphQL(DummyMixin, GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_query(self):
        res = self.query(
            '''
            query{
              allPremiums(sumInsured: 50000, premium: 1200){
                edges{
                  node{
                    percentage
                    sumInsured
                    premium
                  }
                }
              }
            }
            '''
        )
        expected_result = {
            "data": {
                "allPremiums": {
                    "edges": [
                        {
                            "node": {
                                "percentage": 3,
                                "sumInsured": "[7000, None)",
                                "premium": 1500
                            }
                        },
                        {
                            "node": {
                                "percentage": 4,
                                "sumInsured": "[10000, None)",
                                "premium": 2000
                            }
                        }
                    ]
                }
            }
        }
        context = json.loads(res.content)

        self.assertResponseNoErrors(res)
        self.assertDictEqual(expected_result, context)
