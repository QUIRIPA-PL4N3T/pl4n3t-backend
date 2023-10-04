import os

VIDEO_MIME_TYPES = [
    'audio/3gpp2',
    'video/3gpp2',
    'video/x-flv',
    'video/mp4',
    'application/x-mpegURL',
    'video/MP2T',
    'video/3gpp',
    'video/quicktime',
    'video/x-msvideo',
    'video/x-ms-wmv',
    'video/H261',
    'video/H263',
    'video/H263-1998',
    'video/H263-2000',
    'video/H264',
    'video/H264-RCDO',
    'video/H264-SVC',
    'video/H265',
    'video/H266'
]

IMAGE_MIME_TYPES = [
    'image/bmp',
    'image/cis-cod',
    'image/gif',
    'image/ief',
    'image/jpeg',
    'image/pipeg',
    'image/svg+xml',
    'image/tiff',
    'image/x-cmu-raster',
    'image/png',
    'image/x-cmx',
    'image/x-icon',
    'image/x-portable-anymap',
    'image/x-portable-bitmap',
    'image/x-portable-graymap',
    'image/x-portable-pixmap',
    'image/x-rgb',
    'image/x-xpixmap',
    'image/x-xwindowdump',
]

AUDIO_MIME_TYPES = [
    'audio/basic',
    'audio/mid',
    'audio/mpeg',
    'audio/x-aiff',
    'audio/x-mpegurl',
    'audio/x-pn-realaudio',
    'audio/x-pn-realaudio',
    'audio/x-wav',
]

DOCUMENT_MIME_TYPE = [
    'application/pdf',
    'application/msword',
    'application/vnd.ms-excel',
    'application/vnd.ms-excel',
    'application/vnd.ms-excel.addin.macroEnabled.12',
    'application/vnd.ms-excel.sheet.binary.macroEnabled.12',
    'application/vnd.ms-excel.sheet.macroEnabled.12',
    'application/vnd.ms-excel.template.macroEnabled.12',
    'application/vnd.ms-powerpoint',
    'application/vnd.ms-powerpoint.addin.macroEnabled.12',
    'application/vnd.ms-powerpoint.presentation.macroEnabled.12',
    'application/vnd.ms-powerpoint.slide.macroEnabled.12',
    'application/vnd.ms-powerpoint.slideshow.macroEnabled.12',
    'application/vnd.ms-powerpoint.template.macroEnabled.12',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/x-latex',
    'text/plain',
    'text/richtext',
    'text/tab-separated-values',
]

MULTIMEDIA_MIME_TYPES = VIDEO_MIME_TYPES + IMAGE_MIME_TYPES + AUDIO_MIME_TYPES


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


def is_multimedia_file(mime_type: str):
    if mime_type and type(mime_type) == str:
        type_list = mime_type.split('/')
        if len(type_list) > 1:
            return type_list[0] in ['audio', 'video', 'image']
    return False


def get_file_type(mime_type: str):
    if mime_type and type(mime_type) == str:
        if mime_type in DOCUMENT_MIME_TYPE:
            return 'document'
        type_list = mime_type.split('/')
        if len(type_list) > 1:
            return type_list[0]
    return 'unknown'

