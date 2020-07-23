# import io
# import os
#
# import falcon
# from falcon.routing import StaticRoute
# #from .static_resources import _get_template
#
#
# def _open_or_render_template(file_path):
#     ext = os.path.splitext(file_path)[1]
#     if not ext.lower() == '.html':
#         return io.open(file_path, 'rb')
#     else:
#         return bytes(_get_template(file_path).render())
#
#
# class StaticRouteModifier(StaticRoute):
#
#     # Code is almost directly copied from StaticRoute class
#     # Slight modification to the stream return to allow for modification of the source file
#     def __call__(self, req, resp):
#         """Resource responder for this route."""
#
#         without_prefix = req.path[len(self._prefix):]
#
#         # NOTE(kgriffs): Check surrounding whitespace and strip trailing
#         # periods, which are illegal on windows
#         # NOTE(CaselIT): An empty filename is allowed when fallback_filename is provided
#         if (not (without_prefix or self._fallback_filename is not None) or
#                 without_prefix.strip().rstrip('.') != without_prefix or
#                 self._DISALLOWED_CHARS_PATTERN.search(without_prefix) or
#                 '\\' in without_prefix or
#                 '//' in without_prefix or
#                 len(without_prefix) > self._MAX_NON_PREFIXED_LEN):
#
#             raise falcon.HTTPNotFound()
#
#         normalized = os.path.normpath(without_prefix)
#
#         if normalized.startswith('../') or normalized.startswith('/'):
#             raise falcon.HTTPNotFound()
#
#         file_path = os.path.join(self._directory, normalized)
#
#         # NOTE(kgriffs): Final sanity-check just to be safe. This check
#         # should never succeed, but this should guard against us having
#         # overlooked something.
#         if '..' in file_path or not file_path.startswith(self._directory):
#             raise falcon.HTTPNotFound()
#
#         try:
#             resp.stream = _open_or_render_template(file_path)
#         except IOError:
#             if self._fallback_filename is None:
#                 raise falcon.HTTPNotFound()
#             try:
#                 resp.stream = _open_or_render_template(self._fallback_filename)
#                 file_path = self._fallback_filename
#             except IOError:
#                 raise falcon.HTTPNotFound()
#
#         suffix = os.path.splitext(file_path)[1]
#         resp.content_type = resp.options.static_media_types.get(
#             suffix,
#             'application/octet-stream'
#         )
#
#         if self._downloadable:
#             resp.downloadable_as = os.path.basename(file_path)