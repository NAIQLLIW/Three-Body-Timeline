import csv
import json

from matplotlib.font_manager import json_dump


def build_date(row, prefix=''):
    date_dict = {}
    year = row.get(f'{prefix}Year', '').strip()
    if year:
        try:
            date_dict['year'] = int(year)
        except ValueError:
            pass

    month = row.get(f'{prefix}Month', '').strip()
    if month:
        try:
            month_int = int(month)
            if 1 <= month_int <= 12:
                date_dict['month'] = month_int
        except ValueError:
            pass

    day = row.get(f'{prefix}Day', '').strip()
    if day:
        try:
            date_dict['day'] = int(day)
        except ValueError:
            pass

    time_str = row.get(f'{prefix}Time', '').strip()
    if time_str:
        parts = time_str.split(':')
        if parts:
            try:
                hour = int(parts[0])
                if 0 <= hour <= 23:
                    date_dict['hour'] = hour
            except ValueError:
                pass
        if len(parts) > 1:
            try:
                minute = int(parts[1])
                if 0 <= minute <= 59:
                    date_dict['minute'] = minute
            except ValueError:
                pass

    return date_dict if date_dict else None


def build_slide(row):
    slide = {}

    start_date = build_date(row, '')
    if start_date:
        slide['start_date'] = start_date

    end_date = build_date(row, 'End ')
    if end_date:
        slide['end_date'] = end_date

    headline = row.get('Headline', '').strip()
    text_content = row.get('Text', '').strip()
    text_dict = {}
    if headline:
        text_dict['headline'] = headline
    if text_content:
        text_dict['text'] = text_content
    if text_dict:
        slide['text'] = text_dict

    media_url = row.get('Media', '').strip()
    media_caption = row.get('Media Caption', '').strip()
    media_credit = row.get('Media Credit', '').strip()
    media_thumbnail = row.get('Media Thumbnail', '').strip()
    media_alt = row.get('Alt Text', '').strip()
    media_dict = {}
    if media_url:
        media_dict['url'] = media_url
    if media_caption:
        media_dict['caption'] = media_caption
    if media_credit:
        media_dict['credit'] = media_credit
    if media_thumbnail:
        media_dict['thumbnail'] = media_thumbnail
    if media_alt:
        media_dict['alt'] = media_alt
    if media_dict:
        slide['media'] = media_dict

    group = row.get('Group', '').strip()
    if group:
        slide['group'] = group

    display_date = row.get('Display Date', '').strip()
    if display_date:
        slide['display_date'] = display_date

    background = row.get('Background', '').strip()
    if background:
        bg = {}
        if background.startswith(('http://', 'https://')):
            bg['url'] = background
        elif background.startswith('#'):
            bg['color'] = background
        else:
            bg['color'] = background
        slide['background'] = bg

    return slide


def build_era(row):
    era = {}

    start_date = build_date(row, '')
    if start_date:
        era['start_date'] = start_date

    end_date = build_date(row, 'End ')
    if end_date:
        era['end_date'] = end_date

    headline = row.get('Headline', '').strip()
    text_content = row.get('Text', '').strip()
    text_dict = {}
    if headline:
        text_dict['headline'] = headline
    if text_content:
        text_dict['text'] = text_content
    if text_dict:
        era['text'] = text_dict

    return era


def csv_to_json(csv_filename):
    title = None
    events = []
    eras = []

    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_type = row.get('Type', '').strip().lower()
            if row_type == 'title':
                slide = build_slide(row)
                title = slide
            elif row_type == 'era':
                era = build_era(row)
                eras.append(era)
            else:
                slide = build_slide(row)
                if slide:
                    events.append(slide)

    result = {}
    if title is not None:
        result['title'] = title
    if events:
        result['events'] = events
    if eras:
        result['eras'] = eras

    return result


if __name__ == '__main__':
    import sys

    sys.argv.append(r"C:\Users\will\Downloads\Three Body Timeline - TimelineJS3 - od1.csv")
    if len(sys.argv) != 2:
        print("Usage: python script.py input.csv")
        sys.exit(1)

    json_data = csv_to_json(sys.argv[1])
    with open("data.json", "w") as f:
        f.write(json.dumps(json_data, ensure_ascii=False, indent=2))
        