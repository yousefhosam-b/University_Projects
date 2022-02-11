package Project;

public class ListNode {

	String element;
	ListNode link;

	public ListNode(String element) {
		setElement(element);
		link = null;
	}

	public String getElement() {
		return element;
	}

	public void setElement(String element) {
		element = element.toLowerCase();
		this.element = element.substring(0, 1).toUpperCase() + element.substring(1);
	}

	public ListNode getLink() {
		return link;
	}

	public void setLink(ListNode link) {
		this.link = link;
	}
}
