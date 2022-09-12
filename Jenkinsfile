pipeline {
  agent any

  environment {
        GIT_NAME = "eea.facetednavigation"
        SONARQUBE_TAGS = "www.eea.europa.eu"
        FTEST_DIR = "eea/facetednavigation/ftests"
        CUSTOM_FIND = "! -name *.min.js"
    }

  stages {

    stage('Cosmetics') {
      steps {
        parallel(

          "JS Hint": {
            node(label: 'docker') {
              script {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                  sh '''docker run -i --rm --name="$BUILD_TAG-jshint" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/jshint'''
                }
              }
            }
          },

          "CSS Lint": {
            node(label: 'docker') {
              script {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                  sh '''docker run -i --rm --name="$BUILD_TAG-csslint" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/csslint'''
                }
              }
            }
          },

          "PEP8": {
            node(label: 'docker') {
              script {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                  sh '''docker run -i --rm --name="$BUILD_TAG-pep8" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/pep8'''
                }
              }
            }
          },

          "PyLint": {
            node(label: 'docker') {
              script {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                  sh '''docker run -i --rm --name="$BUILD_TAG-pylint" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/pylint'''
                }
              }
            }
          }

        )
      }
    }

    stage('Code') {
      steps {
        parallel(

          "ZPT Lint": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name="$BUILD_TAG-zptlint" -e GIT_BRANCH="$BRANCH_NAME" -e ADDONS="$GIT_NAME" -e DEVELOP="src/$GIT_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/plone-test:4 zptlint'''
            }
          },

          "JS Lint": {
            node(label: 'docker') {
              script {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                  sh '''docker run -i --rm --name="$BUILD_TAG-jslint" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" -e CUSTOM_FIND="$CUSTOM_FIND" eeacms/jslint4java'''
                }
              }
            }
          },

          "PyFlakes": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name="$BUILD_TAG-pyflakes" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/pyflakes'''
            }
          },

          "i18n": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name=$BUILD_TAG-i18n -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/i18ndude'''
            }
          }
        )
      }
    }

    stage('Tests') {
      steps {
        parallel(

          "WWW": {
            node(label: 'docker') {
              script {
                try {
                  sh '''docker run -i --name="$BUILD_TAG-www" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/www-devel /debug.sh coverage'''
                  sh '''mkdir -p xunit-reports; docker cp $BUILD_TAG-www:/plone/instance/parts/xmltestreport/testreports/. xunit-reports/'''
                  stash name: "xunit-reports", includes: "xunit-reports/*.xml"
                  sh '''docker cp $BUILD_TAG-www:/plone/instance/src/$GIT_NAME/coverage.xml coverage.xml'''
                  stash name: "coverage.xml", includes: "coverage.xml"
                } finally {
                  sh '''docker rm -v $BUILD_TAG-www'''
                }
                junit 'xunit-reports/*.xml'
              }
            }
          },


          "KGS": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name="$BUILD_TAG-kgs" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/kgs-devel /debug.sh bin/test --test-path /plone/instance/src/$GIT_NAME -v -vv -s $GIT_NAME'''
            }
          },

          "Plone4": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name="$BUILD_TAG-plone4" -e GIT_BRANCH="$BRANCH_NAME" -e ADDONS="$GIT_NAME" -e DEVELOP="src/$GIT_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/plone-test:4 -v -vv -s $GIT_NAME'''
            }
          },

          "Plone5": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name="$BUILD_TAG-plone5" -e GIT_BRANCH="$BRANCH_NAME" -e ADDONS="$GIT_NAME" -e DEVELOP="src/$GIT_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/plone-test:5 -v -vv -s $GIT_NAME'''
            }
          },

          "Python3": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name="$BUILD_TAG-python3" -e GIT_BRANCH="$BRANCH_NAME" -e ADDONS="$GIT_NAME" -e DEVELOP="src/$GIT_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/plone-test:5-python3 -v -vv -s $GIT_NAME'''
            }
          }
        )
      }
    }

    stage('Functional tests') {
       steps {
         parallel(
          "WWW": {
            node(label: 'docker-host') {
              script {
                try {
                  checkout scm
                  sh '''hostname'''
                  sh '''mkdir -p xunit-functional'''
                  sh '''docker run -d -e ADDONS=$GIT_NAME -e DEVELOP=src/$GIT_NAME -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" --name=$BUILD_TAG-ft-www eeacms/www-devel /debug.sh bin/instance fg'''
                  sh '''timeout 600  wget --retry-connrefused --tries=60 --waitretry=10 -q http://$(docker inspect --format {{.NetworkSettings.IPAddress}} $BUILD_TAG-ft-www):8080/'''
                  sh '''casperjs test $FTEST_DIR/eea/*.js --url=$(docker inspect --format {{.NetworkSettings.IPAddress}} $BUILD_TAG-ft-www):8080 --xunit=xunit-functional/ftestsreport.xml'''
                  stash name: "xunit-functional", includes: "xunit-functional/*.xml"
                } catch (err) {
                  sh '''docker logs --tail=100 $BUILD_TAG-ft-www'''
                  throw err
                } finally {
                  sh '''docker stop $BUILD_TAG-ft-www'''
                  sh '''docker rm -v $BUILD_TAG-ft-www'''
                }
                archiveArtifacts '*.png'
                junit 'xunit-functional/ftestsreport.xml'
              }
            }
          },

          "KGS": {
            node(label: 'docker') {
              script {
                try {
                  checkout scm
                  sh '''docker run -d -e ADDONS=$GIT_NAME -e DEVELOP=src/$GIT_NAME -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" --name=$BUILD_TAG-ft-kgs eeacms/kgs-devel /debug.sh bin/instance fg'''
                  sh '''timeout 600  wget --retry-connrefused --tries=60 --waitretry=10 -q http://$(docker inspect --format {{.NetworkSettings.IPAddress}} $BUILD_TAG-ft-kgs):8080/'''
                  sh '''casperjs test $FTEST_DIR/kgs/*.js --url=$(docker inspect --format {{.NetworkSettings.IPAddress}} $BUILD_TAG-ft-kgs):8080 --xunit=ftestsreport.xml'''
                } catch (err) {
                sh '''docker logs --tail=100 $BUILD_TAG-ft-kgs'''
                throw err
                } finally {
                  sh '''docker stop $BUILD_TAG-ft-kgs'''
                  sh '''docker rm -v $BUILD_TAG-ft-kgs'''
                }
              archiveArtifacts '*.png'
              junit 'ftestsreport.xml'
            }
            }
          },

          // "Plone4": {
          //   node(label: 'docker') {
          //     script {
          //       try {
          //         checkout scm
          //         sh '''docker run -d -e ADDONS=$GIT_NAME -e DEVELOP=src/$GIT_NAME -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" --name=$BUILD_TAG-ft-plone4 eeacms/plone-test:4'''
          //         sh '''timeout 600  wget --retry-connrefused --tries=60 --waitretry=10 -q http://$(docker inspect --format {{.NetworkSettings.IPAddress}} $BUILD_TAG-ft-plone4):8080/'''
          //         sh '''casperjs test $FTEST_DIR/plone4/*.js --url=$(docker inspect --format {{.NetworkSettings.IPAddress}} $BUILD_TAG-ft-plone4):8080 --xunit=ftestsreport.xml'''
          //       } catch (err) {
          //       sh '''docker logs --tail=100 $BUILD_TAG-ft-plone4'''
          //       throw err
          //       } finally {
          //         sh '''docker stop $BUILD_TAG-ft-plone4'''
          //         sh '''docker rm -v $BUILD_TAG-ft-plone4'''
          //       }
          //     }
          //     archiveArtifacts '*.png'
          //     junit 'ftestsreport.xml'
          //     }

          //   }

          )
       }
    }

    stage('Report to SonarQube') {
      // Exclude Pull-Requests
      when {
        allOf {
          environment name: 'CHANGE_ID', value: ''
        }
      }
      steps {
        node(label: 'swarm') {
          script{
            checkout scm
            dir("xunit-reports") {
              unstash "xunit-reports"
            }
            unstash "coverage.xml"
            dir('xunit-functional') {
              unstash "xunit-functional"
            }
            def scannerHome = tool 'SonarQubeScanner';
            def nodeJS = tool 'NodeJS11';
            withSonarQubeEnv('Sonarqube') {
                sh '''sed -i "s|/plone/instance/src/$GIT_NAME|$(pwd)|g" coverage.xml'''
                sh '''find xunit-functional -type f -exec mv {} xunit-reports/ ";"'''
                sh "export PATH=$PATH:${scannerHome}/bin:${nodeJS}/bin; sonar-scanner -Dsonar.python.xunit.skipDetails=true -Dsonar.python.xunit.reportPath=xunit-reports/*.xml -Dsonar.python.coverage.reportPaths=coverage.xml -Dsonar.sources=./eea -Dsonar.projectKey=$GIT_NAME-$BRANCH_NAME -Dsonar.projectVersion=$BRANCH_NAME-$BUILD_NUMBER"
                sh '''try=2; while [ \$try -gt 0 ]; do curl -s -XPOST -u "${SONAR_AUTH_TOKEN}:" "${SONAR_HOST_URL}api/project_tags/set?project=${GIT_NAME}-${BRANCH_NAME}&tags=${SONARQUBE_TAGS},${BRANCH_NAME}" > set_tags_result; if [ \$(grep -ic error set_tags_result ) -eq 0 ]; then try=0; else cat set_tags_result; echo "... Will retry"; sleep 60; try=\$(( \$try - 1 )); fi; done'''
            }
          }
        }
      }
    }

    stage('Pull Request') {
      when {
        not {
          environment name: 'CHANGE_ID', value: ''
        }
        environment name: 'CHANGE_TARGET', value: 'master'
      }
      steps {
        node(label: 'docker') {
          script {
            if ( env.CHANGE_BRANCH != "develop" &&  !( env.CHANGE_BRANCH.startsWith("hotfix")) ) {
                error "Pipeline aborted due to PR not made from develop or hotfix branch"
            }
           withCredentials([string(credentialsId: 'eea-jenkins-token', variable: 'GITHUB_TOKEN')]) {
            sh '''docker run -i --rm --name="$BUILD_TAG-gitflow-pr" -e GIT_CHANGE_BRANCH="$CHANGE_BRANCH" -e GIT_CHANGE_AUTHOR="$CHANGE_AUTHOR" -e GIT_CHANGE_TITLE="$CHANGE_TITLE" -e GIT_TOKEN="$GITHUB_TOKEN" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" -e GIT_ORG="$GIT_ORG" -e GIT_NAME="$GIT_NAME" eeacms/gitflow'''
           }
          }
        }
      }
    }

    stage('Release') {
      when {
        allOf {
          environment name: 'CHANGE_ID', value: ''
          branch 'master'
        }
      }
      steps {
        node(label: 'docker') {
          withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'eea-jenkins', usernameVariable: 'EGGREPO_USERNAME', passwordVariable: 'EGGREPO_PASSWORD'],string(credentialsId: 'eea-jenkins-token', variable: 'GITHUB_TOKEN'),[$class: 'UsernamePasswordMultiBinding', credentialsId: 'pypi-jenkins', usernameVariable: 'PYPI_USERNAME', passwordVariable: 'PYPI_PASSWORD']]) {
            sh '''docker run -i --rm --name="$BUILD_TAG-gitflow-master" -e GIT_BRANCH="$BRANCH_NAME" -e EGGREPO_USERNAME="$EGGREPO_USERNAME" -e EGGREPO_PASSWORD="$EGGREPO_PASSWORD" -e GIT_NAME="$GIT_NAME"  -e PYPI_USERNAME="$PYPI_USERNAME"  -e PYPI_PASSWORD="$PYPI_PASSWORD" -e GIT_ORG="$GIT_ORG" -e GIT_TOKEN="$GITHUB_TOKEN" eeacms/gitflow'''
          }
        }
      }
    }

  }

  post {
    changed {
      script {
        def url = "${env.BUILD_URL}/display/redirect"
        def status = currentBuild.currentResult
        def subject = "${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
        def summary = "${subject} (${url})"
        def details = """<h1>${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - ${status}</h1>
                         <p>Check console output at <a href="${url}">${env.JOB_BASE_NAME} - #${env.BUILD_NUMBER}</a></p>
                      """

        def color = '#FFFF00'
        if (status == 'SUCCESS') {
          color = '#00FF00'
        } else if (status == 'FAILURE') {
          color = '#FF0000'
        }

        emailext (subject: '$DEFAULT_SUBJECT', to: '$DEFAULT_RECIPIENTS', body: details)
      }
    }
  }
}
