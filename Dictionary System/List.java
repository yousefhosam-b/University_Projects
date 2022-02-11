package Project;

public class List {

	ListNode first, last;
	int size;

	public List() {
		first = last = null;
		size = 0;
	}

	public void add(String element) {
		ListNode newnode = new ListNode(element);
		if (first == null) {
			first = last = newnode;
		} else if (first == last) {
			last = newnode;
			first.setLink(last);
		} else {
			last.setLink(newnode);
			last = newnode;
		}

		size += 1;

	}

	public ListNode Search(String element) {
		if (first == null) {
			return null;
		} else {
			ListNode current = first;
			while (current != null) {
				if (current.getElement().toLowerCase().equals(element.toLowerCase())) {
					return current;
				}
				current = current.getLink();
			}
			return null;
		}
	}

	public boolean contains(String element) {
		if (Search(element) != null)
			return true;
		return false;
	}

	public boolean remove(String element) {
		if (!contains(element))
			return false;
		else {
			if (first.getElement().toLowerCase().equals(element.toLowerCase())) {
				if (first == last) {
					first = last = null;
					return true;
				} else {
					ListNode current = first;
					first = first.getLink();
					current.setLink(null);
					return true;
				}
			}

			else {
				ListNode current = first;
				while (current.getLink() != null) {
					if (current.getLink().getElement().toLowerCase().equals(element.toLowerCase())) {
						current.setLink(current.getLink().getLink());
						current.getLink().setLink(null);
						return true;
					}
					current = current.getLink();
				}
			}
			return false;
		}
	}

	public boolean remove(int index) {
		if (size <= index) {
			return false;
		} else {
			if (first == last) {
				first = last = null;
				return true;
			} else {
				ListNode current = first;
				if (index == 0) {
					first = first.getLink();
					current.setLink(null);
					return true;
				} else {
					for (int i = 0; i < size; i++) {
						if (i + 1 == index) {
							current.setLink(current.getLink().getLink());
							current.getLink().setLink(null);
							return true;
						}
						current = current.getLink();
					}
				}

			}
			return false;
		}
	}

	public int size() {
		return size;
	}

	public String toString() {
		String result = "";
		ListNode current = first;
		while (current != null) {
			result += current.getElement();
			current = current.getLink();
			if (current != null) {
				result += ", ";
			}
		}
		return "[" + result + "]";
	}
}
