package Project;

public class AVLNode {

	private String word;
	private List meanings;
	private List synonyms;
	int height;

	AVLNode leftChild, rightChild;

	public AVLNode(String w) {
		setWord(w);
		height = 1;
		meanings = new List();
		synonyms = new List();
	}

	public String getWord() {
		return word;
	}

	public void setWord(String word) {
		word = word.toLowerCase();
		this.word = word.substring(0, 1).toUpperCase() + word.substring(1);
	}

	public List getMeanings() {
		return meanings;
	}

	public void setMeanings(List meanings) {
		ListNode meaning = meanings.first;
		while (meaning != null) {
			if (meaning.getElement().toLowerCase().equals(word.toLowerCase())) {
				meaning = meaning.getLink();
				continue;
			}
			addMeaning(meaning.getElement());
			meaning = meaning.getLink();
		}
	}

	public List getSynonyms() {
		return synonyms;
	}

	public void setSynonyms(List synonyms) {
		ListNode synonym = synonyms.first;
		while (synonym != null) {
			if (synonym.getElement().toLowerCase().equals(word.toLowerCase())) {
				synonym = synonym.getLink();
				continue;
			}
			addSynonym(synonym.getElement());
			synonym = synonym.getLink();
		}
	}

	public void addMeaning(String meaning) {
		meaning = meaning.toLowerCase();
		meaning = meaning.substring(0, 1).toUpperCase() + meaning.substring(1);
		if (!meanings.contains(meaning)) {
			meanings.add(meaning);
		} else
			return;

	}

	public void removeMeaningAt(int index) {
		if (index <= 0)
			return; // There must be at least 1 meaning. For example user will say remove first
					// meaning etc.
		if (index > meanings.size())
			return;

		meanings.remove(index - 1);
	}

	public void addSynonym(String synonym) {
		synonym = synonym.toLowerCase();
		synonym = synonym.substring(0, 1).toUpperCase() + synonym.substring(1);
		if (!synonyms.contains(synonym)) {
			synonyms.add(synonym);
		} else
			return;
	}

	public void removeSynonym(String synonym) {
		synonyms.remove(synonym.toLowerCase());
	}

	public void removeSynonymAt(int index) {
		if (index <= 0)
			return; // There must be at least 1 synonym to use this method. There cannot be negative
					// index also.
		if (index > synonyms.size())
			return; //

		synonyms.remove(index - 1);
	}

	public String toString() {
		return word + "\nMeanings/Anlamlarý:\n" + meanings.toString() + "\nSynonyms/Eþseslileri:\n"
				+ synonyms.toString();
	}

}
