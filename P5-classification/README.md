#P5: CLASSIFICATION

Mục tiêu của Project này là implement 3 classifier: perceptron, MIRA và một classifier perceptron cho pacman.
Đồng thời ta cũng cần tìm các features giúp classifier phân biệt chữ số và các agents của pacman.

3 bài đầu đã được thầy giải quyết trên lớp.
Trong đó, 2 bài 1 và 3 là implement 2 classifier perceptron và MIRA theo mô tả của đề bài.

## 2. Question 2: Perceptron Analysis

Bài 2 là tìm ra 100 features có weight lớn nhất với các chữ số khi chạy classifier perceptron.
Sau khi chạy, các feature hiện ra như hình a.
Do cách viết chữ số là khác nhau, nên các điểm có trọng số lớn nhất là rời rạc chứ không liền mạch như hình b
(Demo)
	python dataClassifier.py -c perceptron -w

## 4. Question 4: Digit Feature Design

Trong bài 4, ta cần xây dựng các features cho classifier phân biệt các chữ số.
Các features cơ bản đã giúp phân biệt đúng 78 trên 100 trường hợp.
Em đã bổ sung thêm feature là số vùng kín của chữ số 
(như theo đề, 1, 2, 3, 5, 7 tend to have one contiguous region of white space while the loops in 6, 8, 9 create more.
The number of white regions in a 4 depends on the writer.) 
Để tìm vùng kín, ta lần lượt xét các điểm trong ô. Nếu điểm đó là điểm trắng, ta lan đen từ điểm đó tới khi gặp viền.
Nếu đó là một vùng kín, việc lan đó sẽ bị giới hạn. Nếu không nõ sẽ lan ra toàn bộ ô đó.
Ta có 4 features tương ứng với số vùng kín như code.
Đếm số vùng kín sau khi tìm được, ta sẽ có feature đủ để đạt yêu cầu đề bài.
(Demo)
	python dataClassifier.py -d digits -c naiveBayes -f -a -t 1000  
		->Kết quả validation set: 83%
		->Kết quả trên test set: 85%>84%
	python autograder.py -q q4
	
## 5. Question 5: Behavioral Cloning

Bài 5 là thay đổi perceptron một chút để làm classifier cho pacman.
Nhìn chung nó không khác quá nhiều, tuy nhiên ta chỉ có 1 w chung cho các trường hợp.
Khi đoán đúng, trọng số sẽ được tăng lên f(s,a) đúng. Ngược lại, nó sẽ bị giảm đi f(s,a′) sai.
(Demo)
	python dataClassifier.py -c perceptron -d pacman
		->Kết quả trên test: 84%

## 6. Question 6: Pacman Feature Design

Bài 6 là thiết kế feature để phân biệt hành vi các agent pacman.
Ở đây, em lựa chọn một số features:
 - Trạng thái hiện tại 
   + thắng hay thua, điểm
   + khoảng cách đến Scared Ghost gần nhất
 - Trạng thái đạt được sau action:
   + khoảng cách đến Ghost gần nhất
   + điểm mới
   + khoảng cách đến Food gần nhất
(Demo)
	python dataClassifier.py -c perceptron -d pacman -f -g ContestAgent -t 1000 -s 1000
		-> với contestAgent, kết quả là 91%
	python dataClassifier.py -c perceptron -d pacman -f -g SuicideAgent -t 1000 -s 1000
		-> với suicideAgent, kết quả là 84%