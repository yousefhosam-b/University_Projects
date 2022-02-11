package Project;

import java.util.Scanner; 

public class CPanel {
	static AVLTree English = new AVLTree();
	static AVLTree Turkish = new AVLTree();
	static Scanner scan = new Scanner(System.in);
	static final String regex = "^\\p{L}+$" ;
	
	public static void main(String[] args) {
		System.out.println("WELCOME TO DICTIONARY SYSTEM!");
		AdminOrUser();
		
	}
	
	static void AdminOrUser() {
		System.out.println("Who are You? -----> (A)dmin or (U)ser or (Q)uit");
		String selection =  scan.nextLine().toLowerCase();
		if (!selection.equals("a") && !selection.equals("u") && !selection.equals("q")) {
			AdminOrUser();
		} 
		else if(selection.equals("a")) {
			DictionarySelection(true);
		}else if (selection.equals("q")) {
			System.out.println("See ya :)");
		}
		else DictionarySelection(false);
		
	}
	static void DictionarySelection(boolean isAdmin) {
			System.out.println("Which dictionary do you want to work with? -----> (E)nglish or (T)urkish or (B)ack");
			String selection = scan.nextLine().toLowerCase();
			if (!selection.equals("e") && !selection.equals("t") && !selection.equals("b")) {
				DictionarySelection(isAdmin);
			} 
			else if(selection.equals("e")) {
				EnglishDic(isAdmin);
			}
			else if(selection.equals("b")) {
				AdminOrUser();
			}
			else {
				TurkishDic(isAdmin);
			}
		
	}
	static void EnglishDic(boolean isAdmin) {
		if (isAdmin) {
			System.out.println("Options:\n" + 
					 "Press c to See Current Words\n" +
					 "Press s to Search a word\n" +
					 "Press w to Add New Word\n" + 
					 "Press d to Delete Word\n" + 
					 "Press q to exit\n");
			String selection = scan.nextLine().toLowerCase();
			String word,meaning,synonym;
			switch (selection) {
			case "c":
				English.inorder(English.root);
				System.out.println();
				EnglishDic(isAdmin);
				break;
			case "w":
				System.out.println("Which word do you want to add?");
				word = scan.nextLine();
				while (!word.matches(regex)) {
					System.out.println("That is not a valid word");
					word = scan.nextLine();
				}
				English.root = English.insert(word , English.root);
				System.out.println("Do you want to add meanings or synonyms to that word? ---> Y / N");
				do {
					 selection = scan.nextLine().toLowerCase();
				} while (!selection.equals("y") && !selection.equals("n"));
				 if (selection.equals("y")) {
					 System.out.println("(M)eanings or Syn(o)nyms?");
					 do {
						 selection = scan.nextLine().toLowerCase();
					} while (!selection.equals("m") && !selection.equals("o"));
					 if (selection.equals("m")) {
						System.out.println("Write the Meaning.");
						meaning = scan.nextLine();
						English.Search(word, English.root).addMeaning(meaning);
						System.out.println("Added");
					} if (selection.equals("o")) {
						System.out.println("Write the Synonym.");
						synonym = scan.nextLine();
						while (!synonym.matches(regex)) {
							System.out.println("That is not a valid word");
							synonym = scan.nextLine();
						}
						English.Search(word, English.root).addSynonym(synonym);
						English.root = English.insert(synonym, English.root);
						English.Search(synonym, English.root).setMeanings(English.Search(word, English.root).getMeanings());
						English.Search(synonym, English.root).setSynonyms(English.Search(word, English.root).getSynonyms());
						English.Search(synonym, English.root).addSynonym(word);
						
					}
				 } EnglishDic(isAdmin);
				break;
			case "s":
				System.out.println("Type the word that you want to search:");
				word = scan.nextLine();
				while (!word.matches(regex)) {
					System.out.println("That is not a valid word");
					word = scan.nextLine();
				}
				if(English.isContains(word, English.root)){
					 System.out.println(word + " is in the dictionary. Do you want to see details of this word? ---> Y / N");
					 do {
						 selection = scan.nextLine().toLowerCase();
					} while (!selection.equals("y") && !selection.equals("n"));
					 if (selection.equals("y")) {
						System.out.println(English.Search(word, English.root).toString());
						System.out.println("Press enter to continue...");try{System.in.read();}catch(Exception e){e.printStackTrace();}
					} 
					System.out.println("Do you want to add meanings or synonyms to that word? ---> Y / N");
						do {
							 selection = scan.nextLine().toLowerCase();
						} while (!selection.equals("y") && !selection.equals("n"));
						 if (selection.equals("y")) {
							 System.out.println("(M)eanings or Syn(o)nyms?");
							 do {
								 selection = scan.nextLine().toLowerCase();
							} while (!selection.equals("m") && !selection.equals("o"));
							 if (selection.equals("m")) {
								System.out.println("Write the Meaning.");
								meaning = scan.nextLine();
								English.Search(word, English.root).addMeaning(meaning);
								System.out.println("Added");
							} if (selection.equals("o")) {
								System.out.println("Write the Synonym.");
								synonym = scan.nextLine();
								while (!synonym.matches(regex)) {
									System.out.println("That is not a valid word");
									synonym = scan.nextLine();
								}
								English.Search(word, English.root).addSynonym(synonym);
								English.root = English.insert(synonym, English.root);
								English.Search(synonym, English.root).setMeanings(English.Search(word, English.root).getMeanings());
								English.Search(synonym, English.root).setSynonyms(English.Search(word, English.root).getSynonyms());
								English.Search(synonym, English.root).addSynonym(word);
								
							}
						 }		 
				}
				else System.out.println(word + " is *not* in the dictionary.");
				EnglishDic(isAdmin);
				break;
			case "d":
				System.out.println("Type the word that you want to delete:");
				word = scan.nextLine();
				while (!word.matches(regex)) {
					System.out.println("That is not a valid word");
					word = scan.nextLine();
				}
				if(English.Search(word, English.root) == null) System.out.println("There is not a word like that.");
				else System.out.println("Deleted " + word);
				English.root = English.deleteNode(word,English.root);
				EnglishDic(isAdmin);
				break;
			case "q":
				System.out.println("Exiting...");
				AdminOrUser();
				break;
			default:
				EnglishDic(isAdmin);
				break;
			}
		} else {
			System.out.println("Options:\n" + 
					 "Press c to See Current Words\n" +
					 "Press s to Search a word\n" +
					 "Press q to exit\n");
			String selection = scan.nextLine().toLowerCase();
			String word;
			switch (selection) {
			case "c":
				English.inorder(English.root);
				System.out.println();
				EnglishDic(isAdmin);
				break;
			case "s":
				System.out.println("Type the word that you want to search:");
				word = scan.nextLine();
				while (!word.matches(regex)) {
					System.out.println("That is not a valid word");
					word = scan.nextLine();
				}
				if(English.isContains(word, English.root)){
					 System.out.println(word + " is in the dictionary. Do you want to see details of this word? ---> Y / N");
					 do {
						 selection = scan.nextLine().toLowerCase();
					} while (!selection.equals("y") && !selection.equals("n"));
					 if (selection.equals("y")) {
						if(English.Search(word, English.root) != null) System.out.println(English.Search(word, English.root).toString());
						System.out.println("Press enter to continue...");try{System.in.read();}catch(Exception e){e.printStackTrace();}
					} 
					 
				}
				else System.out.println(word + " is *not* in the dictionary.");
				EnglishDic(isAdmin);
				break;
			case "q":
				System.out.println("Exiting Application...");
				AdminOrUser();
				break;
			default:
				EnglishDic(isAdmin);
				break;
			}
		}
	}
	static void TurkishDic(boolean isAdmin) {
		if (isAdmin) {
			System.out.println("Se�enekler:\n" + 
					 "Mevcut kelimeleri g�rmek i�in 'c' tu�una bas�n�z\n" +
					 "Kelime aratmak i�in 's' tu�una bas�n�z\n" +
					 "Yeni bir kelime eklemek i�in 'w' tu�una bas�n�z\n" + 
					 "Bir kelimeyi silmek i�in 'd' tu�una bas�n�z\n" + 
					 "��kmak i�in 'q' tu�una bas�n�z\n");
			String selection = scan.nextLine().toLowerCase();
			String word,meaning,synonym;
			switch (selection) {
			case "c":
				Turkish.inorder(Turkish.root);
				System.out.println();
				TurkishDic(isAdmin);
				break;
			case "w":
				System.out.println("Hangi kelimeyi eklemek istiyorsunuz?");
				word = scan.nextLine();
				while (!word.matches(regex)) {
					System.out.println("Bu kelime ge�erli de�il.");
					word = scan.nextLine();
				}
				Turkish.root = Turkish.insert(word , Turkish.root);
				System.out.println("Bu kelimeye anlam veya e�anlaml� s�zc�k eklemek ister misiniz? ---> Y / N");
				do {
					 selection = scan.nextLine().toLowerCase();
				} while (!selection.equals("y") && !selection.equals("n"));
				 if (selection.equals("y")) {
					 System.out.println("Anlam i�in M, E�anlaml� s�zc�k i�in O ya bas�n�z.");
					 do {
						 selection = scan.nextLine().toLowerCase();
					} while (!selection.equals("m") && !selection.equals("o"));
					 if (selection.equals("m")) {
						System.out.println("Anlam� yaz�n.");
						meaning = scan.nextLine();
						Turkish.Search(word, Turkish.root).addMeaning(meaning);
						System.out.println("Eklendi");
					} if (selection.equals("o")) {
						System.out.println("E�anlaml� s�zc��� yaz�n�z.");
						synonym = scan.nextLine();
						while (!synonym.matches(regex)) {
							System.out.println("L�tfen ge�erli bir kelime giriniz");
							synonym = scan.nextLine();
						}
						Turkish.Search(word, Turkish.root).addSynonym(synonym);
						Turkish.root = Turkish.insert(synonym, Turkish.root);
						Turkish.Search(synonym, Turkish.root).setMeanings(Turkish.Search(word, Turkish.root).getMeanings());
						Turkish.Search(synonym, Turkish.root).setSynonyms(Turkish.Search(word, Turkish.root).getSynonyms());
						Turkish.Search(synonym, Turkish.root).addSynonym(word);
					}
				 }TurkishDic(isAdmin);
				break;
			case "s":
				System.out.println("Aratmak istedi�iniz kelimeyi yaz�n�z:");
				word = scan.nextLine();
				while (!word.matches(regex)) {
					System.out.println("Bu ge�erli bir kelime de�il.");
					word = scan.nextLine();
				}
				if(Turkish.isContains(word, Turkish.root)) {
					System.out.println(word + " s�zl�kte mevcut. Kelimenin detaylar�n� g�rmek istermisiniz? ---> Y / N");
					do {
						 selection = scan.nextLine().toLowerCase();
					} while (!selection.equals("y") && !selection.equals("n"));
					 if (selection.equals("y")) {
						System.out.println(Turkish.Search(word, Turkish.root).toString());;
						System.out.println("Devam etmek i�in Enter'a bas�n�z...");try{System.in.read();}catch(Exception e){e.printStackTrace();}
					} 
					System.out.println("Bu kelimeye anlam veya e�anlaml� s�zc�k eklemek ister misiniz? ---> Y / N");
						do {
							 selection = scan.nextLine().toLowerCase();
						} while (!selection.equals("y") && !selection.equals("n"));
						 if (selection.equals("y")) {
							 System.out.println("Anlam i�in M, E�anlaml� s�zc�k i�in O ya bas�n�z.");
							 do {
								 selection = scan.nextLine().toLowerCase();
							} while (!selection.equals("m") && !selection.equals("o"));
							 if (selection.equals("m")) {
								System.out.println("Anlam� yaz�n.");
								meaning = scan.nextLine();
								Turkish.Search(word, Turkish.root).addMeaning(meaning);
								System.out.println("Eklendi");
							} if (selection.equals("o")) {
								System.out.println("E�anlaml� s�zc��� yaz�n�z.");
								synonym = scan.nextLine();
								while (!synonym.matches(regex)) {
									System.out.println("L�tfen ge�erli bir kelime giriniz");
									synonym = scan.nextLine();
								}
								Turkish.Search(word, Turkish.root).addSynonym(synonym);
								Turkish.root = Turkish.insert(synonym, Turkish.root);
								Turkish.Search(synonym, Turkish.root).setMeanings(Turkish.Search(word, Turkish.root).getMeanings());
								Turkish.Search(synonym, Turkish.root).setSynonyms(Turkish.Search(word, Turkish.root).getSynonyms());
								Turkish.Search(synonym, Turkish.root).addSynonym(word);
							}
						 }
				}
				else System.out.println(word + " s�zl�kte bulunamad�.");
				TurkishDic(isAdmin);
				break;
			case "d":
				System.out.println("Silmek istedi�iniz kelimeyi yaz�n�z:");
				word = scan.nextLine();
				while (!word.matches(regex)) {
					System.out.println("Bu kelime ge�erli de�il.");
					word = scan.nextLine();
				}
				if(Turkish.Search(word, Turkish.root) == null) System.out.println("B�yle bir kelime bulunamad�.");
				else System.out.println(word + " silindi.");
				Turkish.root = Turkish.deleteNode(word,Turkish.root);
				TurkishDic(isAdmin);
				break;
			case "q":
				System.out.println("Uygulama kapan�yor...");
				AdminOrUser();
				break;
			default:
				TurkishDic(isAdmin);
				break;
			}
		} else {
			System.out.println("Se�enekler:\n" + 
					 "Mevcut kelimeleri g�rmek i�in 'c' tu�una bas�n�z\n" +
					 "Kelime aratmak i�in 's' tu�una bas�n�z\n" +
					 "��kmak i�in 'q' tu�una bas�n�z\n");
			String selection = scan.nextLine().toLowerCase();
			String word;
			switch (selection) {
			case "c":
				Turkish.inorder(Turkish.root);
				System.out.println();
				TurkishDic(isAdmin);
				break;
			case "s":
				System.out.println("Aratmak istedi�iniz kelimeyi yaz�n�z:");
				word = scan.nextLine();
				while (!word.matches(regex)) {
					System.out.println("Bu ge�erli bir kelime de�il.");
					word = scan.nextLine();
				}
				if(Turkish.isContains(word, Turkish.root)) {
					System.out.println(word + " s�zl�kte mevcut. Kelimenin detaylar�n� g�rmek istermisiniz? ---> Y / N");
					do {
						 selection = scan.nextLine().toLowerCase();
					} while (!selection.equals("y") && !selection.equals("n"));
					 if (selection.equals("y")) {
						System.out.println(Turkish.Search(word, Turkish.root).toString());;
						System.out.println("Devam etmek i�in Enter'a bas�n�z...");try{System.in.read();}catch(Exception e){e.printStackTrace();}
					}
				}
				else System.out.println(word + " s�zl�kte bulunamad�.");
				TurkishDic(isAdmin);
				break;
			case "q":
				System.out.println("��k�l�yor...");
				AdminOrUser();
				break;
			default:
				TurkishDic(isAdmin);
				break;
			}
		}
		
	}
}
