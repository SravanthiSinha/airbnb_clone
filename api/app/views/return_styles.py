"""
This is the return_styles module.
This is a ListStyle class inside the return_styles module.
"""


class ListStyle:
    """
    This is a ListStyle class
    """
    @staticmethod
    def list(select, request):
        """
        Returns a list of resources
        """
        page = request.args.get('page')
        number = request.args.get('number')
        if not page:
            page = 1
        if not number:
            number = 10
        page, number = [int(page), int(number)]
        paging = {}
        if page == 1:
            paging['prev'] = None
        else:
            paging['prev'] = str(request.base_url) + '?page=' + \
                str(page - 1) + '&number=' + str(number)
        paging['next'] = str(request.base_url) + '?page=' + \
            str(page + 1) + '&number=' + str(number)

        list_of_dicts = []
        for row in select.paginate(page, number):
            list_of_dicts.append(row.to_dict())
        return {'data': list_of_dicts, 'paging': paging}
