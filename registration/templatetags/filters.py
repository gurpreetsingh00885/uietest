from django import template

register = template.Library()

@register.filter
def get_full_branch_name(code):
	branches = {
		'IT': 'Information Technology',
		'CS': 'Computer Science & Engineering',
		'EC': 'Electronics & Communication Engineering',
		'EE': 'Electrical & Electronics Engineering',
		'BT': 'Biotechnology',
		'ME': 'Mechanical Engineering',
	}

	return branches[code]

@register.filter
def get_full_year(code):
	years = {
		'1': '1st',
		'2': '2nd',
		'3': '3rd',
		'4': '4th',
	}

	return years[code]

@register.filter
def get_section(code):
	sections = {
		'1': 'A',
		'2': 'B',
	}

	return sections[code]