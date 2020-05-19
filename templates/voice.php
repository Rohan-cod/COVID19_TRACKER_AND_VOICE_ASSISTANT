<html>
<head>
<title>run my python files</title>
<?PHP
  $output = shell_exec("python /Users/rohangupta/Documents/GitHub/COVID19_TRACKER_AND_VOICE_ASSISTANT/tracker/voiceaa.py");
  echo $output;
?>
</head>

<script>
      $(document).ready(function () {

        $('.first-button').on('click', function () {

          $('.animated-icon1').toggleClass('open');
        });
        $('.second-button').on('click', function () {

          $('.animated-icon2').toggleClass('open');
        });
        $('.third-button').on('click', function () {

          $('.animated-icon3').toggleClass('open');
        });
      });
      
    </script>