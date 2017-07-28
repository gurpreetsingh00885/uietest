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