=====
Usage
=====

To use TimeThese in a project::

      from timethese import cmpthese, pprint_cmp, timethese

      xs = range(10)


      def map_hex():
          list(map(hex, xs))


      def list_compr_hex():
          list([hex(x) for x in xs])


      def map_lambda():
          list(map(lambda x: x + 2, xs))


      def map_lambda_fn():
          fn = lambda x: x + 2
          list(map(fn, xs))


      def list_compr_nofn():
          list([x + 2 for x in xs])


      cmp_res_dict = cmpthese(
          10000,
          {
              "map_hex": map_hex,
              "list_compr_hex": list_compr_hex,
              "map_lambda": map_lambda,
              "map_lambda_fn": map_lambda_fn,
              "list_compr_nofn": list_compr_nofn,
          },
          repeat=3,
      )

      print(pprint_cmp(cmp_res_dict))


      cmp_res_list = cmpthese(
          10000, [map_hex, list_compr_hex, map_lambda, map_lambda_fn, list_compr_nofn,], repeat=3,
      )

      print(pprint_cmp(cmp_res_list))
