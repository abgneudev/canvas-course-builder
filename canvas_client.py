"""Canvas LMS API Client
Handles all API interactions with Canvas LMS REST API.
"""
import requests
from typing import Dict, List, Optional, Any


class CanvasClient:
    """Client for interacting with Canvas LMS API."""
    
    def __init__(self, base_url: str, api_token: str):
        """Initialize Canvas client.
        
        Args:
            base_url: Canvas instance URL (e.g., https://canvas.instructure.com)
            api_token: Canvas API access token
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make API request with error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            JSON response data
            
        Raises:
            Exception: If API request fails
        """
        url = f"{self.base_url}/api/v1/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.HTTPError as e:
            error_msg = f"Canvas API error: {e}"
            if hasattr(e.response, 'text'):
                error_msg += f" - {e.response.text}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    # ========== COURSES ==========
    
    def list_courses(self, enrollment_type: Optional[str] = None, 
                     enrollment_state: Optional[str] = None,
                     include: Optional[List[str]] = None) -> List[Dict]:
        """List all courses for the current user.
        
        Args:
            enrollment_type: Filter by enrollment type (teacher, student, ta, etc.)
            enrollment_state: Filter by enrollment state (active, invited, completed)
            include: Additional data to include (syllabus_body, total_scores, etc.)
            
        Returns:
            List of course objects
        """
        params = {}
        if enrollment_type:
            params['enrollment_type'] = enrollment_type
        if enrollment_state:
            params['enrollment_state'] = enrollment_state
        if include:
            params['include[]'] = include
            
        return self._request('GET', 'courses', params=params)
    
    def get_course(self, course_id: int, include: Optional[List[str]] = None) -> Dict:
        """Get a single course by ID.
        
        Args:
            course_id: Course ID
            include: Additional data to include
            
        Returns:
            Course object
        """
        params = {}
        if include:
            params['include[]'] = include
        return self._request('GET', f'courses/{course_id}', params=params)
    
    def create_course(self, account_id: int, name: str, course_code: str,
                      start_at: Optional[str] = None, end_at: Optional[str] = None,
                      license: Optional[str] = None, is_public: bool = False) -> Dict:
        """Create a new course.
        
        Args:
            account_id: Account ID to create course in
            name: Course name
            course_code: Course code
            start_at: Course start date (ISO 8601)
            end_at: Course end date (ISO 8601)
            license: Course license
            is_public: Whether course is public
            
        Returns:
            Created course object
        """
        data = {
            'course': {
                'name': name,
                'course_code': course_code,
                'is_public': is_public
            }
        }
        
        if start_at:
            data['course']['start_at'] = start_at
        if end_at:
            data['course']['end_at'] = end_at
        if license:
            data['course']['license'] = license
            
        return self._request('POST', f'accounts/{account_id}/courses', json=data)
    
    def update_course(self, course_id: int, name: Optional[str] = None,
                      course_code: Optional[str] = None, 
                      event: Optional[str] = None, **kwargs) -> Dict:
        """Update a course.
        
        Args:
            course_id: Course ID
            name: New course name
            course_code: New course code
            event: Course event (offer, claim, conclude, delete, undelete)
            **kwargs: Additional course parameters
            
        Returns:
            Updated course object
        """
        data = {'course': {}}
        
        if name:
            data['course']['name'] = name
        if course_code:
            data['course']['course_code'] = course_code
        if event:
            data['event'] = event
            
        data['course'].update(kwargs)
        
        return self._request('PUT', f'courses/{course_id}', json=data)
    
    def delete_course(self, course_id: int, event: str = 'delete') -> Dict:
        """Delete or conclude a course.
        
        Args:
            course_id: Course ID
            event: 'delete' or 'conclude'
            
        Returns:
            Deleted course object
        """
        return self._request('DELETE', f'courses/{course_id}', params={'event': event})
    
    # ========== MODULES ==========
    
    def list_modules(self, course_id: int, include: Optional[List[str]] = None,
                     include_items: Optional[bool] = None) -> List[Dict]:
        """List all modules in a course.
        
        Args:
            course_id: Course ID
            include: Additional data to include (items, content_details)
            include_items: Whether to include module items in the response
            
        Returns:
            List of module objects
        """
        params = {}
        if include:
            params['include[]'] = include
        if include_items:
            params['include[]'] = params.get('include[]', [])
            # Ensure include[] is a list to append items
            if isinstance(params['include[]'], list):
                params['include[]'].append('items')
            else:
                params['include[]'] = [params['include[]'], 'items']
        return self._request('GET', f'courses/{course_id}/modules', params=params)
    
    def get_module(self, course_id: int, module_id: int, 
                   include: Optional[List[str]] = None) -> Dict:
        """Get a single module.
        
        Args:
            course_id: Course ID
            module_id: Module ID
            include: Additional data to include
            
        Returns:
            Module object
        """
        params = {}
        if include:
            params['include[]'] = include
        return self._request('GET', f'courses/{course_id}/modules/{module_id}', params=params)
    
    def create_module(self, course_id: int, name: str, position: Optional[int] = None,
                      unlock_at: Optional[str] = None, 
                      require_sequential_progress: bool = False,
                      prerequisite_module_ids: Optional[List[int]] = None,
                      publish_final_grade: bool = False) -> Dict:
        """Create a new module.
        
        Args:
            course_id: Course ID
            name: Module name
            position: Module position in course
            unlock_at: Module unlock date (ISO 8601)
            require_sequential_progress: Require students to complete items in order
            prerequisite_module_ids: List of prerequisite module IDs
            publish_final_grade: Publish grade when module is complete
            
        Returns:
            Created module object
        """
        data = {
            'module': {
                'name': name,
                'require_sequential_progress': require_sequential_progress,
                'publish_final_grade': publish_final_grade
            }
        }
        
        if position is not None:
            data['module']['position'] = position
        if unlock_at:
            data['module']['unlock_at'] = unlock_at
        if prerequisite_module_ids:
            data['module']['prerequisite_module_ids[]'] = prerequisite_module_ids
            
        return self._request('POST', f'courses/{course_id}/modules', json=data)
    
    def update_module(self, course_id: int, module_id: int, 
                      name: Optional[str] = None, **kwargs) -> Dict:
        """Update a module.
        
        Args:
            course_id: Course ID
            module_id: Module ID
            name: New module name
            **kwargs: Additional module parameters
            
        Returns:
            Updated module object
        """
        data = {'module': {}}
        if name:
            data['module']['name'] = name
        data['module'].update(kwargs)
        
        return self._request('PUT', f'courses/{course_id}/modules/{module_id}', json=data)
    
    def delete_module(self, course_id: int, module_id: int) -> Dict:
        """Delete a module.
        
        Args:
            course_id: Course ID
            module_id: Module ID
            
        Returns:
            Deleted module object
        """
        return self._request('DELETE', f'courses/{course_id}/modules/{module_id}')
    
    def create_module_item(self, course_id: int, module_id: int, title: str, 
                          item_type: str, content_id: Optional[int] = None,
                          position: Optional[int] = None, indent: int = 0,
                          page_url: Optional[str] = None, 
                          external_url: Optional[str] = None) -> Dict:
        """Create a module item.
        
        Args:
            course_id: Course ID
            module_id: Module ID
            title: Item title
            item_type: Type (File, Page, Discussion, Assignment, Quiz, SubHeader, ExternalUrl, ExternalTool)
            content_id: ID of the content object
            position: Item position in module
            indent: Indentation level (0-3)
            page_url: Page URL (for Page type)
            external_url: External URL (for ExternalUrl type)
            
        Returns:
            Created module item object
        """
        data = {
            'module_item': {
                'title': title,
                'type': item_type,
                'indent': indent
            }
        }
        
        if content_id is not None:
            data['module_item']['content_id'] = content_id
        if position is not None:
            data['module_item']['position'] = position
        if page_url:
            data['module_item']['page_url'] = page_url
        if external_url:
            data['module_item']['external_url'] = external_url
            
        return self._request('POST', f'courses/{course_id}/modules/{module_id}/items', json=data)
    
    # ========== PAGES ==========
    
    def list_pages(self, course_id: int, search_term: Optional[str] = None,
                   published: Optional[bool] = None) -> List[Dict]:
        """List all pages in a course.
        
        Args:
            course_id: Course ID
            search_term: Search pages by title
            published: Filter by published status
            
        Returns:
            List of page objects
        """
        params = {}
        if search_term:
            params['search_term'] = search_term
        if published is not None:
            params['published'] = published
            
        return self._request('GET', f'courses/{course_id}/pages', params=params)
    
    def get_page(self, course_id: int, url_or_id: str) -> Dict:
        """Get a single page.
        
        Args:
            course_id: Course ID
            url_or_id: Page URL or ID
            
        Returns:
            Page object
        """
        return self._request('GET', f'courses/{course_id}/pages/{url_or_id}')
    
    def create_page(self, course_id: int, title: str, body: str,
                    editing_roles: str = 'teachers', notify_of_update: bool = False,
                    published: bool = True, front_page: bool = False) -> Dict:
        """Create a new page.
        
        Args:
            course_id: Course ID
            title: Page title
            body: Page content (HTML)
            editing_roles: Who can edit (teachers, students, members, public)
            notify_of_update: Notify users of page creation
            published: Publish page immediately
            front_page: Set as course front page
            
        Returns:
            Created page object
        """
        data = {
            'wiki_page': {
                'title': title,
                'body': body,
                'editing_roles': editing_roles,
                'notify_of_update': notify_of_update,
                'published': published,
                'front_page': front_page
            }
        }
        
        return self._request('POST', f'courses/{course_id}/pages', json=data)
    
    def update_page(self, course_id: int, url_or_id: str, 
                    title: Optional[str] = None, body: Optional[str] = None,
                    published: Optional[bool] = None, **kwargs) -> Dict:
        """Update a page.
        
        Args:
            course_id: Course ID
            url_or_id: Page URL or ID
            title: New page title
            body: New page content
            published: Update published status
            **kwargs: Additional page parameters
            
        Returns:
            Updated page object
        """
        data = {'wiki_page': {}}
        
        if title:
            data['wiki_page']['title'] = title
        if body:
            data['wiki_page']['body'] = body
        if published is not None:
            data['wiki_page']['published'] = published
            
        data['wiki_page'].update(kwargs)
        
        return self._request('PUT', f'courses/{course_id}/pages/{url_or_id}', json=data)
    
    def delete_page(self, course_id: int, url_or_id: str) -> Dict:
        """Delete a page.
        
        Args:
            course_id: Course ID
            url_or_id: Page URL or ID
            
        Returns:
            Deleted page object
        """
        return self._request('DELETE', f'courses/{course_id}/pages/{url_or_id}')
    
    # ========== ASSIGNMENTS ==========
    
    def list_assignments(self, course_id: int, search_term: Optional[str] = None,
                         bucket: Optional[str] = None, 
                         order_by: str = 'position') -> List[Dict]:
        """List all assignments in a course.
        
        Args:
            course_id: Course ID
            search_term: Search assignments by name
            bucket: Filter by bucket (past, overdue, undated, ungraded, upcoming, future)
            order_by: Order results (position, name, due_at)
            
        Returns:
            List of assignment objects
        """
        params = {'order_by': order_by}
        if search_term:
            params['search_term'] = search_term
        if bucket:
            params['bucket'] = bucket
            
        return self._request('GET', f'courses/{course_id}/assignments', params=params)
    
    def get_assignment(self, course_id: int, assignment_id: int, 
                       include: Optional[List[str]] = None) -> Dict:
        """Get a single assignment.
        
        Args:
            course_id: Course ID
            assignment_id: Assignment ID
            include: Additional data to include
            
        Returns:
            Assignment object
        """
        params = {}
        if include:
            params['include[]'] = include
        return self._request('GET', f'courses/{course_id}/assignments/{assignment_id}', params=params)
    
    def create_assignment(self, course_id: int, name: str, 
                          submission_types: Optional[List[str]] = None,
                          points_possible: Optional[float] = None,
                          due_at: Optional[str] = None, 
                          description: Optional[str] = None,
                          published: bool = False,
                          grading_type: str = 'points',
                          **kwargs) -> Dict:
        """Create a new assignment.
        
        Args:
            course_id: Course ID
            name: Assignment name
            submission_types: List of submission types (online_text_entry, online_url, 
                            online_upload, media_recording, etc.)
            points_possible: Maximum points
            due_at: Due date (ISO 8601)
            description: Assignment description (HTML)
            published: Publish assignment immediately
            grading_type: Grading type (points, pass_fail, percent, letter_grade, gpa_scale)
            **kwargs: Additional assignment parameters
            
        Returns:
            Created assignment object
        """
        data = {
            'assignment': {
                'name': name,
                'published': published,
                'grading_type': grading_type
            }
        }
        
        if submission_types:
            data['assignment']['submission_types'] = submission_types
        if points_possible is not None:
            data['assignment']['points_possible'] = points_possible
        if due_at:
            data['assignment']['due_at'] = due_at
        if description:
            data['assignment']['description'] = description
            
        data['assignment'].update(kwargs)
        
        return self._request('POST', f'courses/{course_id}/assignments', json=data)
    
    def update_assignment(self, course_id: int, assignment_id: int,
                          name: Optional[str] = None, **kwargs) -> Dict:
        """Update an assignment.
        
        Args:
            course_id: Course ID
            assignment_id: Assignment ID
            name: New assignment name
            **kwargs: Additional assignment parameters
            
        Returns:
            Updated assignment object
        """
        data = {'assignment': {}}
        if name:
            data['assignment']['name'] = name
        data['assignment'].update(kwargs)
        
        return self._request('PUT', f'courses/{course_id}/assignments/{assignment_id}', json=data)
    
    def delete_assignment(self, course_id: int, assignment_id: int) -> Dict:
        """Delete an assignment.
        
        Args:
            course_id: Course ID
            assignment_id: Assignment ID
            
        Returns:
            Deleted assignment object
        """
        return self._request('DELETE', f'courses/{course_id}/assignments/{assignment_id}')
    
    # ========== DISCUSSIONS ==========
    
    def list_discussions(self, course_id: int, search_term: Optional[str] = None,
                        order_by: str = 'position') -> List[Dict]:
        """List all discussion topics in a course.
        
        Args:
            course_id: Course ID
            search_term: Search discussions by title
            order_by: Order results (position, recent_activity, title)
            
        Returns:
            List of discussion topic objects
        """
        params = {'order_by': order_by}
        if search_term:
            params['search_term'] = search_term
            
        return self._request('GET', f'courses/{course_id}/discussion_topics', params=params)
    
    def get_discussion(self, course_id: int, topic_id: int) -> Dict:
        """Get a single discussion topic.
        
        Args:
            course_id: Course ID
            topic_id: Discussion topic ID
            
        Returns:
            Discussion topic object
        """
        return self._request('GET', f'courses/{course_id}/discussion_topics/{topic_id}')
    
    def create_discussion(self, course_id: int, title: str, message: str,
                          discussion_type: str = 'side_comment',
                          published: bool = True, is_announcement: bool = False,
                          pinned: bool = False, require_initial_post: bool = False,
                          assignment: Optional[Dict] = None) -> Dict:
        """Create a new discussion topic.
        
        Args:
            course_id: Course ID
            title: Discussion title
            message: Discussion message (HTML)
            discussion_type: Type (side_comment, threaded)
            published: Publish immediately
            is_announcement: Create as announcement
            pinned: Pin discussion
            require_initial_post: Require initial post before viewing replies
            assignment: Assignment parameters for graded discussion
            
        Returns:
            Created discussion topic object
        """
        data = {
            'title': title,
            'message': message,
            'discussion_type': discussion_type,
            'published': published,
            'is_announcement': is_announcement,
            'pinned': pinned,
            'require_initial_post': require_initial_post
        }
        
        if assignment:
            data['assignment'] = assignment
            
        return self._request('POST', f'courses/{course_id}/discussion_topics', json=data)
    
    def update_discussion(self, course_id: int, topic_id: int,
                          title: Optional[str] = None, message: Optional[str] = None,
                          **kwargs) -> Dict:
        """Update a discussion topic.
        
        Args:
            course_id: Course ID
            topic_id: Discussion topic ID
            title: New discussion title
            message: New discussion message
            **kwargs: Additional discussion parameters
            
        Returns:
            Updated discussion topic object
        """
        data = {}
        if title:
            data['title'] = title
        if message:
            data['message'] = message
        data.update(kwargs)
        
        return self._request('PUT', f'courses/{course_id}/discussion_topics/{topic_id}', json=data)
    
    def delete_discussion(self, course_id: int, topic_id: int) -> Dict:
        """Delete a discussion topic.
        
        Args:
            course_id: Course ID
            topic_id: Discussion topic ID
            
        Returns:
            Deleted discussion topic object
        """
        return self._request('DELETE', f'courses/{course_id}/discussion_topics/{topic_id}')
    
    def post_discussion_entry(self, course_id: int, topic_id: int, 
                             message: str) -> Dict:
        """Post an entry to a discussion topic.
        
        Args:
            course_id: Course ID
            topic_id: Discussion topic ID
            message: Entry message (HTML)
            
        Returns:
            Created discussion entry object
        """
        data = {'message': message}
        return self._request('POST', f'courses/{course_id}/discussion_topics/{topic_id}/entries', 
                           json=data)
    
    # ========== QUIZZES ==========
    
    def list_quizzes(self, course_id: int, search_term: Optional[str] = None) -> List[Dict]:
        """List all quizzes in a course.
        
        Args:
            course_id: Course ID
            search_term: Search quizzes by title
            
        Returns:
            List of quiz objects
        """
        params = {}
        if search_term:
            params['search_term'] = search_term
            
        return self._request('GET', f'courses/{course_id}/quizzes', params=params)
    
    def get_quiz(self, course_id: int, quiz_id: int) -> Dict:
        """Get a single quiz.
        
        Args:
            course_id: Course ID
            quiz_id: Quiz ID
            
        Returns:
            Quiz object
        """
        return self._request('GET', f'courses/{course_id}/quizzes/{quiz_id}')
    
    def create_quiz(self, course_id: int, title: str, 
                    quiz_type: str = 'assignment', description: Optional[str] = None,
                    time_limit: Optional[int] = None, 
                    shuffle_answers: bool = False,
                    allowed_attempts: int = 1, scoring_policy: str = 'keep_highest',
                    published: bool = False, due_at: Optional[str] = None,
                    **kwargs) -> Dict:
        """Create a new quiz.
        
        Args:
            course_id: Course ID
            title: Quiz title
            quiz_type: Type (practice_quiz, assignment, graded_survey, survey)
            description: Quiz description (HTML)
            time_limit: Time limit in minutes
            shuffle_answers: Shuffle answer order
            allowed_attempts: Number of attempts allowed (-1 for unlimited)
            scoring_policy: How to score (keep_highest, keep_latest, keep_average)
            published: Publish immediately
            due_at: Due date (ISO 8601)
            **kwargs: Additional quiz parameters
            
        Returns:
            Created quiz object
        """
        data = {
            'quiz': {
                'title': title,
                'quiz_type': quiz_type,
                'shuffle_answers': shuffle_answers,
                'allowed_attempts': allowed_attempts,
                'scoring_policy': scoring_policy,
                'published': published
            }
        }
        
        if description:
            data['quiz']['description'] = description
        if time_limit:
            data['quiz']['time_limit'] = time_limit
        if due_at:
            data['quiz']['due_at'] = due_at
            
        data['quiz'].update(kwargs)
        
        return self._request('POST', f'courses/{course_id}/quizzes', json=data)
    
    def update_quiz(self, course_id: int, quiz_id: int, 
                    title: Optional[str] = None, **kwargs) -> Dict:
        """Update a quiz.
        
        Args:
            course_id: Course ID
            quiz_id: Quiz ID
            title: New quiz title
            **kwargs: Additional quiz parameters
            
        Returns:
            Updated quiz object
        """
        data = {'quiz': {}}
        if title:
            data['quiz']['title'] = title
        data['quiz'].update(kwargs)
        
        return self._request('PUT', f'courses/{course_id}/quizzes/{quiz_id}', json=data)
    
    def delete_quiz(self, course_id: int, quiz_id: int) -> Dict:
        """Delete a quiz.
        
        Args:
            course_id: Course ID
            quiz_id: Quiz ID
            
        Returns:
            Deleted quiz object
        """
        return self._request('DELETE', f'courses/{course_id}/quizzes/{quiz_id}')
    
    # ========== ANNOUNCEMENTS ==========
    
    def create_announcement(self, course_id: int, title: str, message: str,
                           published: bool = True) -> Dict:
        """Create an announcement (special type of discussion).
        
        Args:
            course_id: Course ID
            title: Announcement title
            message: Announcement message (HTML)
            published: Publish immediately
            
        Returns:
            Created announcement object
        """
        return self.create_discussion(
            course_id=course_id,
            title=title,
            message=message,
            published=published,
            is_announcement=True
        )
